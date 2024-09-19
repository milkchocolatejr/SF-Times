WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (200, 200, 200)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (200, 200, 0)
BG_COLOR = DARKGREY

WIDTH = 600
HEIGHT = 800
FPS = 60
TITLE = "State Farm Worlde"

#TILE_SIZE = 80
def tile_size(letters):
    return int(100 - ((letters - 4) * 8))

GAP_SIZE = 10

GUESSES = 5


def margin_x(letters):
    return int((WIDTH - (letters * (tile_size(letters) + GAP_SIZE))) / 2)


def margin_y(letters):
    return int((HEIGHT - (letters * (tile_size(letters) + GAP_SIZE))) / 2)
