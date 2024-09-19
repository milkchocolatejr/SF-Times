import pygame
import random

from hackday.Connections import operations

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = (600, 600)
GRID_SIZE = 4
BUTTON_SIZE_X = 120
BUTTON_SIZE_Y = 80
PADDING = 20
BUTTON_COLOR = (33, 33, 33)
SELECTED_COLOR = (150, 150, 150)
SUBMIT_COLOR = (189, 79, 108)
SHUFFLE_COLOR = (3, 166, 136)
CLEAR_COLOR = (184, 15, 15)
GROUP_COLORS = [
    (249, 223, 109),  # Group 1 color (red)
    (160, 195, 90),   # Group 2 color (green)
    (176, 196, 239),  # Group 3 color (blue)
    (186, 129, 197)   # Group 4 color (yellow)
]

# Initialize the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Connections')

# Font for button text
font = pygame.font.Font("Akrobat-SemiBold.otf", 26)
font_title = pygame.font.Font("Frutiger Bold Italic.ttf", 42)
font_title2 = pygame.font.Font("Frutiger Bold Italic.ttf", 42)

# Create a grid of buttons
buttons = []
selected_buttons = []
past_guess = ['data']
completed_buttons = []
top_groups = []

color_iter = 0
message = ""
incorrect_guesses = 0
max_incorrect_guesses = 5

# Simulating your operations.data() call with sample data
fields = operations.data()

groups = list(x for y in fields.values() for x in y)
group_colors = random.sample(GROUP_COLORS, GRID_SIZE)


def generate_buttons():
    global buttons
    buttons = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(
                j * (BUTTON_SIZE_X + PADDING) + PADDING,
                i * (BUTTON_SIZE_Y + PADDING) + PADDING + 50,
                BUTTON_SIZE_X,
                BUTTON_SIZE_Y
            )
            buttons.append(rect)


def draw_buttons():
    global completed_buttons, font
    y_offset = 50

    for group in top_groups:
        rect = pygame.Rect(
            PADDING,
            y_offset,
            SCREEN_SIZE[0] - 2 * PADDING,
            BUTTON_SIZE_Y
        )
        pygame.draw.rect(screen, group['color'], rect)
        text = font.render(group['name'], True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

        button_text = " ".join(group['labels'])
        button_label = font.render(button_text, True, (0, 0, 0))
        button_label_rect = button_label.get_rect(center=(rect.centerx, rect.centery + 20))
        screen.blit(button_label, button_label_rect)

        y_offset += BUTTON_SIZE_Y + PADDING

    remaining_buttons = [btn for btn in buttons if btn not in completed_buttons]

    for i, rect in enumerate(remaining_buttons):
        color = BUTTON_COLOR
        if rect in selected_buttons:
            color = SELECTED_COLOR

        rect.y = (len(top_groups) * (BUTTON_SIZE_Y + PADDING)) + ((i // GRID_SIZE) * (BUTTON_SIZE_Y + PADDING)) + 50
        rect.x = (i % GRID_SIZE) * (BUTTON_SIZE_X + PADDING) + PADDING
        pygame.draw.rect(screen, color, rect)

        button_text = str(groups[buttons.index(rect)])

        # Calculate the appropriate font size
        font_size = operations.get_dynamic_font_size("Akrobat-SemiBold.otf", button_text, rect.width-15, rect.height-15, 26)
        dynamic_font = pygame.font.Font("Akrobat-SemiBold.otf", font_size)

        text_surface = dynamic_font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)


def draw_message():
    global message
    message_text = font.render(message, True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]-30))
    screen.blit(message_text, message_rect)


def submit_selection():
    global selected_buttons, top_groups, color_iter, message, incorrect_guesses, past_guess
    message = ""
    if len(selected_buttons) == 4:
        group_set = [groups[buttons.index(btn)] for btn in selected_buttons]
        setF = [set(x) for x in fields.values()]
        print(set(past_guess) - set(group_set))
        if set(past_guess) - set(group_set) == set():
            message = "Cannot submit same guess twice in a row"
        elif set(group_set) in setF:
            past_guess = group_set
            group_name = next(name for name, items in fields.items() if set(items) == set(group_set))
            test_highlight(group_name)
            selected_buttons.clear()
        else:
            past_guess = group_set
            _=0
            for x in setF:
                if len(set(group_set) & x) >= 3:
                    message = "One away..."
                    _=1
                    break
                else:
                    message = "Selected buttons are not from the same group."
                    _=1
            if _: incorrect_guesses += 1
    else:
        message = "Please select 4 tiles"
    print(message)
    check_game_over()


def adjust_positions():
    global buttons, completed_buttons, top_groups

    if top_groups:
        # Calculate how many rows have been moved to the top
        num_rows = sum(len(group['buttons']) // GRID_SIZE for group in top_groups)

        for i, button in enumerate(completed_buttons):
            # Calculate the position of the button after moving rows to the top
            row = i // GRID_SIZE
            col = i % GRID_SIZE
            button.y = row * (BUTTON_SIZE_Y + PADDING) + PADDING + 50 + num_rows * (BUTTON_SIZE_Y + PADDING)
            button.x = col * (BUTTON_SIZE_X + PADDING) + PADDING


def test_highlight(group_name):
    global buttons, selected_buttons, color_iter, top_groups, completed_buttons
    selected_indices = [buttons.index(btn) for btn in selected_buttons]
    selected_rects = [buttons[i] for i in selected_indices]
    selected_labels = [groups[i] for i in selected_indices]
    top_groups.append({
        'buttons': selected_rects,
        'labels': selected_labels,
        'color': GROUP_COLORS[color_iter],
        'name': group_name
    })
    color_iter += 1
    completed_buttons.extend(selected_rects)

    adjust_positions()
    check_game_over()


def shuffle_buttons():
    global message, completed_buttons
    clear_selection()
    message = ""
    remaining_buttons = [btn for btn in buttons if btn not in completed_buttons]

    remaining_indices = [buttons.index(btn) for btn in remaining_buttons]
    remaining_groups = [groups[i] for i in remaining_indices]

    random.shuffle(remaining_groups)

    for i, index in enumerate(remaining_indices):
        groups[index] = remaining_groups[i]


def clear_selection():
    global message
    message = ""
    selected_buttons.clear()


def check_game_over():
    global running, incorrect_guesses, top_groups
    if len(top_groups) == GRID_SIZE:
        show_end_screen("You Win!")
    elif incorrect_guesses >= max_incorrect_guesses:
        show_end_screen("You Lose")


def show_end_screen(text):
    global running
    end_screen = True
    while end_screen:
        screen.fill((0, 0, 0))
        end_text = font_title.render(text, True, (255, 255, 255))
        end_rect = end_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 50))
        screen.blit(end_text, end_rect)

        restart_rect = pygame.Rect((SCREEN_SIZE[0] // 2) - 75, (SCREEN_SIZE[1] // 2) + 10, 150, 50)
        quit_rect = pygame.Rect((SCREEN_SIZE[0] // 2) - 75, (SCREEN_SIZE[1] // 2) + 70, 150, 50)

        pygame.draw.rect(screen, (0, 255, 0), restart_rect)
        restart_text = font.render("Restart", True, (0, 0, 0))
        restart_rect_text = restart_text.get_rect(center=restart_rect.center)
        screen.blit(restart_text, restart_rect_text)

        pygame.draw.rect(screen, (255, 0, 0), quit_rect)
        quit_text = font.render("Quit", True, (0, 0, 0))
        quit_rect_text = quit_text.get_rect(center=quit_rect.center)
        screen.blit(quit_text, quit_rect_text)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_screen = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    end_screen = False
                elif quit_rect.collidepoint(event.pos):
                    running = False
                    end_screen = False


def reset_game():
    global buttons, selected_buttons, completed_buttons, top_groups, color_iter, message, incorrect_guesses
    generate_buttons()
    shuffle_buttons()
    selected_buttons.clear()
    completed_buttons.clear()
    top_groups.clear()
    color_iter = 0
    message = ""
    incorrect_guesses = 0


# Main loop
generate_buttons()
running = True
shuffle_buttons()
while running:
    screen.fill((0, 0, 0))

    title_text2 = font_title2.render("SF Connections", True, (255, 255, 255))
    title_rect2 = title_text2.get_rect(center=(SCREEN_SIZE[0] // 2, 25))
    screen.blit(title_text2, title_rect2)
    title_text = font_title.render("SF Connections", True, (237, 29, 36))
    title_rect = title_text.get_rect(center=((SCREEN_SIZE[0] // 2) - 2, 23))
    screen.blit(title_text, title_rect)

    # Draw submit button
    submit_rect = pygame.Rect((SCREEN_SIZE[0] // 2) - 50, SCREEN_SIZE[1]-100, 100, 50)  # 130x
    pygame.draw.rect(screen, SUBMIT_COLOR, submit_rect)
    submit_text = font.render("Submit", True, (0, 0, 0))
    submit_rect = submit_text.get_rect(center=submit_rect.center)
    screen.blit(submit_text, submit_rect)

    # Draw shuffle button
    shuffle_rect = pygame.Rect((SCREEN_SIZE[0] // 2) - 180, SCREEN_SIZE[1]-100, 100, 50)
    pygame.draw.rect(screen, SHUFFLE_COLOR, shuffle_rect)
    shuffle_text = font.render("Shuffle", True, (0, 0, 0))
    shuffle_rect = shuffle_text.get_rect(center=shuffle_rect.center)
    screen.blit(shuffle_text, shuffle_rect)

    # Draw clear button
    clear_rect = pygame.Rect((SCREEN_SIZE[0] // 2) + 80, SCREEN_SIZE[1]-100, 100, 50)
    pygame.draw.rect(screen, CLEAR_COLOR, clear_rect)
    clear_text = font.render("Clear", True, (0, 0, 0))
    clear_rect = clear_text.get_rect(center=clear_rect.center)
    screen.blit(clear_text, clear_rect)

    draw_buttons()
    draw_message()

    guesses_text = "Guesses Remaining: " + "o " * (max_incorrect_guesses - incorrect_guesses) + "x " * incorrect_guesses
    guesses_text_rendered = font.render(guesses_text.strip(), True, (255, 255, 255))
    guesses_rect = guesses_text_rendered.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 135))
    screen.blit(guesses_text_rendered, guesses_rect)

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if submit_rect.collidepoint(mouse_pos):
                submit_selection()
            elif shuffle_rect.collidepoint(mouse_pos):
                shuffle_buttons()
            elif clear_rect.collidepoint(mouse_pos):
                clear_selection()
            else:
                for button in buttons:
                    if button.collidepoint(mouse_pos):
                        if button in completed_buttons:
                            continue
                        elif button in selected_buttons:
                            selected_buttons.remove(button)
                        else:
                            if len(selected_buttons) < 4:
                                selected_buttons.append(button)

pygame.quit()
