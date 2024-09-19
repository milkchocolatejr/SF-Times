import pygame
import random

from hackday.Connections import operations

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = (600, 700)
GRID_SIZE = 4
BUTTON_SIZE_X = 120
BUTTON_SIZE_Y = 80
PADDING = 20
BUTTON_COLOR = (100, 100, 100)
SELECTED_COLOR = (0, 255, 0)
SUBMIT_COLOR = (0, 255, 255)
SHUFFLE_COLOR = (255, 255, 0)
CLEAR_COLOR = (255, 0, 0)
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
font = pygame.font.Font(None, 36)

# Create a grid of buttons
buttons = []
selected_buttons = []
completed_buttons = []
top_groups = []

color_iter = 0
message = ""

# Mockup for operations.data() because it is not provided
fields = operations.data()


# Create groups for the buttons
groups = list(x for y in fields.values() for x in y)
group_colors = random.sample(GROUP_COLORS, GRID_SIZE)

# Generate buttons
def generate_buttons():
    global buttons, groups, group_colors
    buttons.clear()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(
                j * (BUTTON_SIZE_X + PADDING) + PADDING,
                i * (BUTTON_SIZE_Y + PADDING) + PADDING + 50,
                BUTTON_SIZE_X,
                BUTTON_SIZE_Y
            )
            buttons.append(rect)

# Draw buttons
def draw_buttons():
    global message

    # Draw buttons
    for rect in buttons:
        color = BUTTON_COLOR
        if rect in selected_buttons:
            color = SELECTED_COLOR
        elif rect in completed_buttons:
            color = GROUP_COLORS[0]
        pygame.draw.rect(screen, color, rect)
        index = buttons.index(rect)
        text = font.render(str(groups[index]), True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()

# Submit selection
def submit_selection():
    global selected_buttons, top_groups, color_iter, message
    if len(selected_buttons) == 4:
        group_set = [groups[buttons.index(btn)] for btn in selected_buttons]
        if set(group_set) in [set(x) for x in fields.values()]:
            group_name = next(name for name, items in fields.items() if set(items) == set(group_set))
            test_highlight(group_name)
            selected_buttons.clear()
        else:
            message = "One away..."
    else:
        message = "Please select 4 tiles"
    print(message)

# Test highlight
def test_highlight(group_name):
    global buttons, selected_buttons, color_iter, top_groups
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
    completed_buttons.append(selected_buttons)
    for x in selected_buttons:
        buttons.pop(buttons.index(x))

# Shuffle buttons
def shuffle_buttons():
    global message
    message = ""
    remaining_buttons = [btn for btn in buttons if btn not in completed_buttons]
    remaining_indices = [buttons.index(btn) for btn in remaining_buttons]
    remaining_groups = [groups[i] for i in remaining_indices]

    random.shuffle(remaining_groups)

    for i, index in enumerate(remaining_indices):
        groups[index] = remaining_groups[i]

# Clear selection
def clear_selection():
    global message
    message = ""
    selected_buttons.clear()

# Main loop
generate_buttons()
running = True
while running:
    screen.fill((0, 0, 0))

    # Draw submit button
    submit_rect = pygame.Rect(50, 600, 100, 50)
    pygame.draw.rect(screen, SUBMIT_COLOR, submit_rect)
    submit_text = font.render("Submit", True, (255, 255, 255))
    screen.blit(submit_text, submit_rect.move(10, 10))

    # Draw shuffle button
    shuffle_rect = pygame.Rect(180, 600, 100, 50)
    pygame.draw.rect(screen, SHUFFLE_COLOR, shuffle_rect)
    shuffle_text = font.render("Shuffle", True, (0, 0, 0))
    screen.blit(shuffle_text, shuffle_rect.move(10, 10))

    # Draw clear button
    clear_rect = pygame.Rect(310, 600, 100, 50)
    pygame.draw.rect(screen, CLEAR_COLOR, clear_rect)
    clear_text = font.render("Clear", True, (255, 255, 255))
    screen.blit(clear_text, clear_rect.move(10, 10))

    # Draw message
    message_text = font.render(message, True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 30))
    screen.blit(message_text, message_rect)


    draw_buttons()

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
