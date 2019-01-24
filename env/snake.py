import pygame
import random
from env.pixel import Pixel
from env.config import *

head = 0
tail = -1
init_length = 3

class Snake(object):

    def __init__(self):
        a = LEFT
        self.body = []
        self._born()


    def _born(self):
        head_x = random.randint(WALL_THICKNESS + 1, SCREEN_WIDTH // PIXEL_SIZE - init_length - WALL_THICKNESS)
        head_y = random.randint(WALL_THICKNESS + 1, SCREEN_HEIGHT // PIXEL_SIZE - init_length - WALL_THICKNESS)
        self.body.insert(0, Pixel(head_x, head_y))
        for i in range(init_length - 1):
            part = Pixel(self.body[head].x + i + 1, self.body[head].y)
            self.body.append(part)
    
    @property
    def head(self):
        return self.body[head]


    @property
    def direction(self):
        if self.body[head].x < self.body[head + 1].x:
            return LEFT
        elif self.body[head].x > self.body[head + 1].x:
            return RIGHT
        elif self.body[head].y < self.body[head + 1].y:
            return UP
        else:
            return DOWN


    def growup(self):
        self.body.append(self.body[tail])
    

    def move(self):
        current_direction = self.direction
        del self.body[tail]
        if current_direction == LEFT:
            new_head = Pixel(self.body[head].x - 1, self.body[head].y)
            self.body.insert(0, new_head)
        elif current_direction == RIGHT:
            new_head = Pixel(self.body[head].x + 1, self.body[head].y)            
            self.body.insert(0, new_head)
        elif current_direction == UP:
            new_head = Pixel(self.body[head].x, self.body[head].y - 1)            
            self.body.insert(0, new_head)
        else:
            new_head = Pixel(self.body[head].x, self.body[head].y + 1)                
            self.body.insert(0, new_head)
    

    def turn(self, direction):
        if direction == LEFT:
            self.turn_to_left()
            return True
        elif direction == RIGHT:
            self.turn_to_right()
            return True
        elif direction == UP:
            self.turn_to_up()
            return True
        else:
            self.turn_to_down()
            return True
        return False
    

    def turn_to_up(self):
        del self.body[-1]
        new_head = Pixel(self.body[head].x, self.body[head].y - 1)
        self.body.insert(0, new_head)


    def turn_to_down(self):
        del self.body[-1]
        new_head = Pixel(self.body[head].x, self.body[head].y + 1)
        self.body.insert(0, new_head)


    def turn_to_left(self):
        del self.body[-1]
        new_head = Pixel(self.body[head].x - 1, self.body[head].y)
        self.body.insert(0, new_head)


    def turn_to_right(self):
        del self.body[-1]
        new_head = Pixel(self.body[head].x + 1, self.body[head].y)
        self.body.insert(0, new_head)
    

    def turn_left(self):
        direction = self.direction
        if direction == LEFT:
            self.turn_to_down()
        elif direction == UP:
            self.turn_to_left()
        elif direction == RIGHT:
            self.turn_to_up()
        elif direction == DOWN:
            self.turn_to_right()


    def turn_right(self):
        direction = self.direction
        if direction == LEFT:
            self.turn_to_up()
        elif direction == UP:
            self.turn_to_right()
        elif direction == RIGHT:
            self.turn_to_down()
        elif direction == DOWN:
            self.turn_to_left()