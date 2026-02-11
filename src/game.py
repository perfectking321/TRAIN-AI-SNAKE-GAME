import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import os

pygame.init()
# Get the font path relative to project root
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
_font_path = os.path.join(_project_root, 'assets', 'arial.ttf')
font = pygame.font.Font(_font_path, 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 5000

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
         # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.prev_distance = None  # Track distance to food for reward shaping
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Calculate distance to food before moving
        if self.prev_distance is None:
            self.prev_distance = self._get_distance_to_food()
        prev_dist = self.prev_distance
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        
        # Check collision type for better rewards
        wall_collision = self._is_wall_collision(self.head)
        tail_collision = self._is_tail_collision(self.head)
        
        # Removed timeout check (100*len(self.snake)) to allow Hamiltonian cycle to complete
        if wall_collision or tail_collision:
            game_over = True
            if tail_collision:
                reward = -15  # Stronger penalty for biting tail (harder to avoid)
            else:
                reward = -10  # Wall collision
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10  # Food reward
            self._place_food()
            self.prev_distance = None  # Reset distance tracking
        else:
            self.snake.pop()
            
            # Reward shaping: encourage moving towards food
            current_dist = self._get_distance_to_food()
            if current_dist < prev_dist:
                reward = 1  # Small reward for getting closer to food
            else:
                reward = -1  # Small penalty for moving away from food
            self.prev_distance = current_dist
            
            # TAIL SAFETY REWARD: Encourage keeping safe distance from tail
            if len(self.snake) > 3:  # Only matters when snake is long enough
                min_tail_distance = self._get_min_distance_to_tail()
                
                if min_tail_distance <= BLOCK_SIZE:
                    # Danger zone! Very close to tail
                    reward -= 2  # Warning penalty
                elif min_tail_distance <= 2 * BLOCK_SIZE:
                    # Close to tail but not critical
                    reward -= 0.5  # Small penalty
                else:
                    # Safe distance from tail
                    reward += 0.1  # Tiny reward for being safe
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def _get_distance_to_food(self):
        """Calculate Manhattan distance from head to food"""
        if self.food is None:
            return 0
        return abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)
    
    def _get_min_distance_to_tail(self):
        """Calculate minimum Manhattan distance from head to any tail segment"""
        if len(self.snake) <= 3:
            return float('inf')  # No tail to worry about
        
        min_dist = float('inf')
        # Check distance to tail segments (skip first 3 segments as they're too close by design)
        for segment in self.snake[3:]:
            dist = abs(self.head.x - segment.x) + abs(self.head.y - segment.y)
            min_dist = min(min_dist, dist)
        return min_dist
    
    def _is_wall_collision(self, pt):
        """Check if point collides with walls"""
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        return False
    
    def _is_tail_collision(self, pt):
        """Check if point collides with snake's own body"""
        if pt in self.snake[1:]:
            return True
        return False
    
    def is_collision(self, pt=None):
        """Check if point collides with walls or tail"""
        if pt is None:
            pt = self.head
        return self._is_wall_collision(pt) or self._is_tail_collision(pt)
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        
        if self.food is not None:
            pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] #right turn r->d->l->u
        else: #[0,0,1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] #right turn r->u->l->d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            