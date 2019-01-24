import random
from env.pixel import Pixel
from env.config import *


class Apple(object):

    def __init__(self):
        self.location = Pixel(0, 0)

    def reposition(self, snake):
        pxs = []
        for x in range(WALL_THICKNESS, SCREEN_WIDTH // PIXEL_SIZE - WALL_THICKNESS):
            for y in range(WALL_THICKNESS, SCREEN_HEIGHT // PIXEL_SIZE - WALL_THICKNESS):
                pxs.append(Pixel(x, y))
        
        for i in range(0, len(snake.body) - 1):
            px = Pixel(snake.body[i].x, snake.body[i].y)
            if px in pxs:
                pxs.remove(px)
        
        new_position_index = random.randint(WALL_THICKNESS, len(pxs) - 1)
        new_position = pxs[new_position_index]
        self.location = new_position