import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import os

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT  = 2
    UP    = 3
    DOWN  = 4

Point = namedtuple('Point', 'x, y')

WHITE  = (255, 255, 255)
RED    = (200,   0,   0)
BLUE1  = (  0,   0, 255)
BLUE2  = (  0, 100, 255)
BLACK  = (  0,   0,   0)

BLOCK_SIZE = 20
SPEED      = 40   # frames per second; raise to train faster


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()
        # Init font after pygame is fully ready
        try:
            _font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'arial.ttf')
            self.font = pygame.font.Font(_font_path, 25)
        except Exception:
            try:
                self.font = pygame.font.SysFont('arial', 25)
            except Exception:
                self.font = None
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head  = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE,     self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
        self.score          = 0
        self.food           = None
        self.frame_iteration = 0
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._move(action)
        self.snake.insert(0, self.head)

        reward    = 0
        game_over = False

        # Death: wall or self-collision, or taking too long
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward    = -10
            return reward, game_over, self.score

        # Ate food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Wall
        if pt.x >= self.w or pt.x < 0 or pt.y >= self.h or pt.y < 0:
            return True
        # Self
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        if self.font:
            self.display.blit(self.font.render('Score: ' + str(self.score), True, WHITE), [0, 0])
        pygame.display.flip()

    def _move(self, action):
        cw  = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = cw.index(self.direction)
        if   np.array_equal(action, [1, 0, 0]): new_dir = cw[idx]
        elif np.array_equal(action, [0, 1, 0]): new_dir = cw[(idx + 1) % 4]
        else:                                    new_dir = cw[(idx - 1) % 4]
        self.direction = new_dir

        x, y = self.head.x, self.head.y
        if   self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:  x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:  y += BLOCK_SIZE
        elif self.direction == Direction.UP:    y -= BLOCK_SIZE
        self.head = Point(x, y)
            