import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot
import os
import json


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate - IMPORTANT: considers future rewards
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        
        # Initialize model and trainer
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
        # Load previous best model if exists
        self.record = 0
        self.load_model()

    def load_model(self):
        """Load the best saved model and its metadata"""
        model_folder_path = './model'
        metadata_path = os.path.join(model_folder_path, 'metadata.json')
        
        # Try to load the model
        try:
            if self.model.load():
                # Load metadata if exists
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            self.record = metadata.get('record', 0)
                            self.n_games = metadata.get('n_games', 0)
                            print(f'\n=== Resuming Training ===')
                            print(f'Previous Record: {self.record}')
                            print(f'Games Played: {self.n_games}')
                            print(f'Previous Mean Score: {metadata.get("mean_score", 0):.2f}')
                            print(f'Last Training: {metadata.get("timestamp", "Unknown")}')
                            print('========================\n')
                    except Exception as e:
                        print(f'Error loading metadata: {e}')
            else:
                print('No previous model found. Starting fresh training.')
        except RuntimeError as e:
            if "size mismatch" in str(e):
                print('\n⚠️  Saved model incompatible (size mismatch - may be from hybrid agent)')
                print('Starting fresh training with pure AI agent.\n')
            else:
                raise


    def get_state(self,game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self,state,action,reward, next_state, done):
        self.memory.append((state,action,reward, next_state, done)) #popleft if MAX_MEMORY

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # return list of tuples
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards, next_states, dones)


    def train_short_memory(self,state,action,reward, next_state, done):
        self.trainer.train_step(state,action,reward, next_state, done)

    def get_action(self,state):
        # Improved exploration strategy
        # Early games: high exploration (random moves)
        # Later games: more exploitation (use learned policy)
        self.epsilon = 80 - self.n_games  # Reduced from 90 for faster convergence
        final_moves = [0,0,0]
        
        # Exploration: random moves with decreasing probability
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_moves[move] = 1
        else:
            # Exploitation: use the neural network's prediction
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = int(torch.argmax(prediction).item())
            final_moves[move] = 1
            
        return final_moves

def train():
    plot_scores = []
    plot_mean_scores = []

    total_score = 0
    agent = Agent()
    game = SnakeGameAI()
    
    # Start with the loaded record
    record = agent.record
    
    # Adjust total_score based on loaded games for accurate mean calculation
    if agent.n_games > 0:
        print(f'Continuing from game {agent.n_games + 1}...\n')
    
    while True:
        #get old state
        state_old = agent.get_state(game)
        #get move
        final_move = agent.get_action(state_old)
        #perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if done:
            #train the long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            # Update total score for this game
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / len(plot_scores)
            plot_mean_scores.append(mean_score)
            
            if score > record:
                record = score
                # Save with metadata when new record is achieved
                agent.model.save(record=record, n_games=agent.n_games, mean_score=mean_score)
                print(f'🎉 New Record! Score: {record}')
            else:
                # Still save periodically (every 10 games) to preserve progress
                if agent.n_games % 10 == 0:
                    agent.model.save(record=record, n_games=agent.n_games, mean_score=mean_score)
                    print(f'✓ Progress saved at game {agent.n_games}')

            print(f'Game {agent.n_games} | Score: {score} | Record: {record}')
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()