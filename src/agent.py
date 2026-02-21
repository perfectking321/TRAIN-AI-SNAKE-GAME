import torch
import random
import numpy as np
from collections import deque
from .game import Direction, Point
from .model import Linear_QNet, QTrainer
import os
import json

MAX_MEMORY = 100_000
BATCH_SIZE  = 1_000
LR          = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0      # exploration rate (decreases over time)
        self.gamma   = 0.9    # discount rate
        self.memory  = deque(maxlen=MAX_MEMORY)
        self.record  = 0

        # Network: 11 state inputs → 256 hidden → 3 actions
        self.model   = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load(self):
        try:
            if self.model.load():
                meta = './model/metadata.json'
                if os.path.exists(meta):
                    with open(meta) as f:
                        d = json.load(f)
                    self.record  = d.get('record',  0)
                    self.n_games = d.get('n_games', 0)
                    print(f'Resuming from game {self.n_games} | Record: {self.record}')
        except RuntimeError:
            print('Saved model incompatible — starting fresh.')

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------
    def get_state(self, game):
        head = game.snake[0]
        pl = Point(head.x - 20, head.y)
        pr = Point(head.x + 20, head.y)
        pu = Point(head.x, head.y - 20)
        pd = Point(head.x, head.y + 20)

        dl = game.direction == Direction.LEFT
        dr = game.direction == Direction.RIGHT
        du = game.direction == Direction.UP
        dd = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dr and game.is_collision(pr)) or (dl and game.is_collision(pl)) or
            (du and game.is_collision(pu)) or (dd and game.is_collision(pd)),
            # Danger right
            (du and game.is_collision(pr)) or (dd and game.is_collision(pl)) or
            (dl and game.is_collision(pu)) or (dr and game.is_collision(pd)),
            # Danger left
            (dd and game.is_collision(pr)) or (du and game.is_collision(pl)) or
            (dr and game.is_collision(pu)) or (dl and game.is_collision(pd)),
            # Current direction
            dl, dr, du, dd,
            # Food location
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y,
        ]
        return np.array(state, dtype=int)

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        sample = random.sample(self.memory, BATCH_SIZE) if len(self.memory) > BATCH_SIZE else self.memory
        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    # ------------------------------------------------------------------
    # Action  (epsilon-greedy)
    # ------------------------------------------------------------------
    def get_action(self, state):
        # Explore more early on, exploit the network more later
        self.epsilon = 80 - self.n_games
        move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move[random.randint(0, 2)] = 1
        else:
            pred = self.model(torch.tensor(state, dtype=torch.float))
            move[int(torch.argmax(pred).item())] = 1
        return move

if __name__ == '__main__':
    train()