import sys
import pygame
import numpy as np
from pygame.locals import *
from env.color import Colors
from env.pixel import Pixel
from env.snake import Snake
from env.apple import Apple
from env.environment import Environment
from env.config import *

class SnakeGame(object):

    def __init__(self, is_tick=False):
        pygame.init()
        global screen, FPS
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        FPS = pygame.time.Clock()
        self.is_tick = is_tick
        self._build_enviroment()


    def _build_enviroment(self):
        self.environment = Environment(SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_SIZE)
        self.snake = Snake()
        self.apple = Apple()
        self.apple.reposition(self.snake)
        self.score = 0
    
    @property
    def observation_shape(self):
        return np.shape(self.environment.pixels)

    def new_round(self):
        self._build_enviroment()
        feedback = Feedback(
            observation=np.copy(self.environment.pixels),
            reward=0,
            game_over=False
        )
        return feedback

    def step(self, action):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if self.is_tick:
            FPS.tick(10)
        
        if action == MOVE_ON:
            self.snake.move()
        elif action == TURN_LEFT:
            self.snake.turn_left()
        elif action == TURN_RIGHT:
            self.snake.turn_right()

        eat_apple = self.eat_apple(self.snake, self.apple)
        game_over = self.game_is_over(self.snake)

        if game_over is False:
            self.render()

        reward = 1 if eat_apple is True else 0
        if game_over:
            reward = -1
        
        feedback = Feedback(
            observation=np.copy(self.environment.pixels),
            reward=reward,
            game_over=game_over
        )

        return feedback

    @property
    def actions_num(self):
        return len(SNAKE_ACTIONS)
    
    @property
    def current_score(self):
        return self.score    

    def draw_node(self, x, y, px):
        rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        if px == Pixel.WALL:
            pygame.draw.rect(screen, Colors.WALL, rect)
        elif px == Pixel.APPLE:
            pygame.draw.rect(screen, Colors.APPLE, rect)
        elif px == Pixel.SNAKE_HEAD:
            pygame.draw.rect(screen, Colors.SNAKE_HEAD, rect)
        elif px == Pixel.SNAKE_BODY:
            pygame.draw.rect(screen, Colors.SNAKE_BODY, rect)
    
    def draw_environment(self, environment):
        screen.fill((Colors.BLANK))
        w, h = environment.shape
        for i in range(w):
            for j in range(h):
                self.draw_node(i, j, environment.read_pixel(i, j))

    def render(self):
        self.update_enviroment(self.snake,self.apple, self.environment)
        self.draw_environment(self.environment)
        pygame.display.update()

    def update_enviroment(self, snake, apple, environment):
        environment.reset()
        for px in snake.body:
            environment.write_pixel(Pixel(px.x, px.y), Pixel.SNAKE_BODY)
        environment.write_pixel(snake.head, Pixel.SNAKE_HEAD)
        environment.write_pixel(Pixel(apple.location.x, apple.location.y), Pixel.APPLE)
    
    def eat_apple(self, snake, apple):
        if snake.head.x == apple.location.x and snake.head.y == apple.location.y:
            snake.growup()
            apple.reposition(snake)
            self.score += 1
            return True
        return False

    def game_is_over(self, snake):
        if snake.head.x * PIXEL_SIZE < WALL_THICKNESS * PIXEL_SIZE or snake.head.x * PIXEL_SIZE >= SCREEN_WIDTH - PIXEL_SIZE or snake.head.y * PIXEL_SIZE < WALL_THICKNESS * PIXEL_SIZE or snake.head.y * PIXEL_SIZE >= SCREEN_HEIGHT - PIXEL_SIZE:
            return True
        else:
            for part in snake.body[1:]:
                if part == snake.head:
                    return True
        return False

    def gameOver(self):
        screen.fill((0, 0, 0))
        fontObj = pygame.font.Font('freesansbold.ttf', 20)
        textSurfaceObj1 = fontObj.render('Game over!', True, (255, 0, 0))
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
        screen.blit(textSurfaceObj1, textRectObj1)

        textSurfaceObj2 = fontObj.render('Score: %s' % self.score, True, (255, 0, 0))
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (SCREEN_WIDTH*2/3, SCREEN_HEIGHT*2/3)
        screen.blit(textSurfaceObj2, textRectObj2)

        pygame.display.update()

        over = True
        while(over):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


    def destroy(self):
        pygame.quit()
        sys.exit()

class Feedback(object):

    def __init__(self, observation, reward, game_over):
        self.observation = observation,
        self.reward = reward,
        self.game_over = game_over