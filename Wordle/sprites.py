import pygame
from settings import *


class Tile:
    def __init__(self, x, y, size, letter='', color=None):
        self.x, self.y = x, y
        self.letter = letter
        self.color = color
        self.width, self.height = size, size
        self.font_size = int(60 * (size / 100))
        self.create_font()

    def create_font(self):
        font = pygame.font.SysFont("Consolas", self.font_size)
        self.render_letter = font.render(self.letter, True, WHITE)
        self.font_width, self.font_height = font.size(self.letter)

    def draw(self, screen):
        if self.color is None:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        if self.letter != "":
            self.font_x = self.x + (self.width / 2) - (self.font_width / 2)
            self.font_y = self.y + (self.height / 2) - (self.font_height / 2)
            letter = pygame.transform.scale(self.render_letter, (int(self.font_width), int(self.font_height)))
            screen.blit(letter, (self.font_x, self.font_y))
