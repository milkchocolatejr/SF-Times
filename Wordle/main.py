import pygame
from words import *
from sprites import *
from settings import *



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def new(self):
        self.word = get_word()
        self.text = ""
        self.current_row = 0
        self.tiles = []
        self.create_tiles()
        self.flip = True

    def create_tiles(self):
        for row in range(GUESSES):
            self.tiles.append([])
            for col in range(len(self.word)):
                self.tiles[row].append(Tile((col * (tile_size(len(self.word)) + GAP_SIZE)) + margin_x(len(self.word)), (row * (tile_size(len(self.word)) + GAP_SIZE)) + margin_y(len(self.word)), tile_size(len(self.word))))

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def temp_alert(self, message, duration):
        # Draw alert box
        alert_box_width = 300
        alert_box_height = 100
        alert_box_rect = pygame.Rect((WIDTH - alert_box_width) // 2, (HEIGHT - alert_box_height) // 2, alert_box_width, alert_box_height)
        pygame.draw.rect(self.screen, RED, alert_box_rect)

        # Draw message text
        text = self.font.render(message, True, WHITE)
        text_rect = text.get_rect(center=alert_box_rect.center)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(duration)  # Wait for the specified duration

    def update(self):
        self.add_letter()

    def add_letter(self):
        for tile in self.tiles[self.current_row]:
            tile.letter = ""

        for i, letter in enumerate(self.text):
            self.tiles[self.current_row][i].letter = letter
            self.tiles[self.current_row][i].create_font()

    def box_animation(self):
        for tile in self.tiles[self.current_row]:
            if tile.letter == "":
                screen_copy = self.screen.copy()

                # First phase of animation: expand
                for size in range(0, 7, 2):  # Increase by 2 from 0 to 6
                    self.screen.blit(screen_copy, (0, 0))
                    tile.x -= size
                    tile.y -= size
                    tile.width += size * 2
                    tile.height += size * 2
                    surface = pygame.Surface((tile.width, tile.height))
                    surface.fill(BG_COLOR)
                    self.screen.blit(surface, (tile.x, tile.y))
                    tile.draw(self.screen)
                    pygame.display.flip()
                    self.clock.tick(FPS)
                self.add_letter()
                # Second phase of animation: contract
                for size in range(6, -1, -2):  # Decrease by 2 from 6 to 0
                    self.screen.blit(screen_copy, (0, 0))
                    tile.x += size
                    tile.y += size
                    tile.width -= size * 2
                    tile.height -= size * 2
                    surface = pygame.Surface((tile.width, tile.height))
                    surface.fill(BG_COLOR)
                    self.screen.blit(surface, (tile.x, tile.y))
                    tile.draw(self.screen)
                    pygame.display.flip()
                    self.clock.tick(FPS)
                break

    def check_letters(self):
        copy_word = [x for x in self.word]
        for i, user_letter in enumerate(self.text):
            color = LIGHTGREY
            for j, letter in enumerate(copy_word):
                if user_letter == letter:
                    color = YELLOW
                    if i == j:
                        color = GREEN
                    copy_word[j] = ""
                    break
            self.reveal_animation(self.tiles[self.current_row][i], color)
    def reveal_animation(self, tile, color):
        screen_copy = self.screen.copy()

        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(BG_COLOR)
            screen_copy.blit(surface, (tile.x, tile.y))
            self.screen.blit(screen_copy, (0,0))
            if self.flip:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.color = color
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
            if tile.font_height == 0:
                self.flip = False

            tile.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            if tile.font_height == tile.font_size:
                self.flip = True
                break


    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_tiles()
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.text) == len(self.word) and is_english_word(self.text):
                        #TODO: Check if the word is valid from the list
                        self.check_letters()
                        #TODO: Check correctness

                        #Win Condition
                        if self.text == self.word:
                            #TODO: Send win condition
                            self.temp_alert("GOOD NEIGHBOR ALERT!!", 5000)
                            pygame.display.update()
                            self.playing = False
                            break
                        #Lose Condition
                        elif self.current_row + 1 == 6:
                            self.temp_alert("Better luck next time.", 5000)
                            pygame.display.update()
                            self.playing = False
                            break

                        self.current_row += 1
                        self.text = ""
                    else:
                        #TODO: Row shake animation
                        if len(self.text) != len(self.word):
                            self.temp_alert("Not enough letters!", 1000)
                            pygame.display.update()

                        elif not is_english_word(self.text):
                            self.temp_alert("Not a valid word!", 1000)
                            pygame.display.update()
                        self.current_row += 0

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < len(self.word) and event.unicode.isalpha():
                        self.text += event.unicode.upper()
                        self.box_animation()

game = Game()

while True:
    game.new()
    game.run()