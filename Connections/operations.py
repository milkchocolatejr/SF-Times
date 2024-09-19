import csv
import random

import pygame

DATAFILE = "data.csv"


def getGroups():
    with open(DATAFILE, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
        fields = []

        while len(fields) != 4:
            ran = random.randrange(len(data))
            if not data[ran] in fields:
                fields.append(data[ran])

        return fields


def data():
    fields = getGroups()

    sorted = {
        fields[0][0]: random.sample(fields[0][1:],4),
        fields[1][0]: random.sample(fields[1][1:],4),
        fields[2][0]: random.sample(fields[2][1:],4),
        fields[3][0]: random.sample(fields[3][1:],4)
    }

    return sorted

def get_dynamic_font_size(font, text, max_width, max_height, max_font_size):
    font_size = min(max_width, max_height, max_font_size)  # Start with the maximum possible size
    while font_size > 0:
        test_font = pygame.font.Font(font, font_size)
        text_surface = test_font.render(text, True, (255, 255, 255))
        if text_surface.get_width() <= max_width and text_surface.get_height() <= max_height:
            break
        font_size -= 1
    return font_size
