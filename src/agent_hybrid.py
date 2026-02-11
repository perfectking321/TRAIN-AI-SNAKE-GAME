"""
Hybrid Agent: Combines Deep Q-Learning with Hamiltonian Safety Net
"""

import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot
from hamiltonian_path import HamiltonianPath
import os
import json


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class HybridAgent:
    """
    Agent that uses AI learning but falls back to Hamiltonian cycle when in danger
    """
    
    def __init__(self, use_hamiltonian=True, model_path='./model_hybrid'):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        
        # Use separate model folder for hybrid agent to avoid conflicts
        self.model_folder = model_path
        
        # Initialize model and trainer with expanded state (11 + 3 Hamiltonian features = 14)
        self.model = Linear_QNet(14, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
        # Hamiltonian path system
        self.use_hamiltonian = use_hamiltonian
        self.hamiltonian = HamiltonianPath(640, 480, 20) if use_hamiltonian else None
        
        # Safety thresholds
        self.danger_threshold = 0.3  # Use Hamiltonian when safety < 30%
        self.min_exploration_games = 50  # Always explore for first 50 games
        
        # Statistics
        self.hamiltonian_uses = 0
        self.ai_decisions = 0
        self.record = 0
        
        # Load previous model
        self.load_model()
    
    def load_model(self):
        """Load the best saved model and its metadata"""
        model_folder_path = self.model_folder
        metadata_path = os.path.join(model_folder_path, 'metadata.json')
        
        # Create model folder if it doesn't exist
        os.makedirs(model_folder_path, exist_ok=True)
        
        # Try to load the model
        try:
            if self.model.load(folder=model_folder_path):
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            self.record = metadata.get('record', 0)
                            self.n_games = metadata.get('n_games', 0)
                            print(f'\n=== Resuming Hybrid Training ===')
                            print(f'Previous Record: {self.record}')
                            print(f'Games Played: {self.n_games}')
                            print(f'Hamiltonian Safety: {"ENABLED" if self.use_hamiltonian else "DISABLED"}')
                            print('================================\n')
                    except Exception as e:
                        print(f'Error loading metadata: {e}')
            else:
                print('No previous hybrid model found. Starting fresh training.')
                print(f'Hamiltonian Safety: {"ENABLED" if self.use_hamiltonian else "DISABLED"}\n')
        except RuntimeError as e:
            if "size mismatch" in str(e):
                print('\n⚠️  Model size mismatch - starting fresh')
                print('Starting new training with hybrid model.')
                print(f'Hamiltonian Safety: {"ENABLED" if self.use_hamiltonian else "DISABLED"}\n')
            else:
                raise
    
    def get_state(self, game):
        """
        Get enhanced state with Hamiltonian features
        
        Returns:
            14-element state array:
            - 11 original features (dangers, direction, food location)
            - 3 Hamiltonian features (on_path, distance_to_food, safety_score)
        """
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # Original 11 features
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
            game.food.y > game.head.y   # food down
        ]
        
        # Add Hamiltonian features (3 features)
        if self.use_hamiltonian:
            ham_features = self.hamiltonian.get_hamiltonian_state_features(
                head, game.food, game.snake
            )
            state.extend(ham_features)
        else:
            state.extend([0, 0, 0])  # Dummy features if Hamiltonian disabled

        return np.array(state, dtype=float)
    
    def calculate_danger_level(self, game):
        """
        Calculate current danger level
        
        Returns:
            Danger score (0-1, higher is more dangerous)
        """
        head = game.snake[0]
        
        # Check immediate dangers
        danger_count = 0
        total_checks = 0
        
        # Check all 4 directions
        for dx, dy in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
            point = Point(head.x + dx, head.y + dy)
            total_checks += 1
            if game.is_collision(point):
                danger_count += 1
        
        immediate_danger = danger_count / total_checks
        
        # Check if trapped (3 or 4 sides blocked)
        if danger_count >= 3:
            return 1.0  # Maximum danger
        
        # Check proximity to tail
        min_tail_distance = float('inf')
        if len(game.snake) > 3:
            for segment in game.snake[3:]:
                dist = abs(head.x - segment.x) + abs(head.y - segment.y)
                min_tail_distance = min(min_tail_distance, dist)
            
            if min_tail_distance <= 20:  # Very close to tail
                immediate_danger += 0.3
        
        return min(1.0, immediate_danger)
    
    def should_use_hamiltonian(self, game):
        """
        Decide whether to use Hamiltonian cycle or AI decision
        
        Returns:
            True if should use Hamiltonian, False if use AI
        """
        if not self.use_hamiltonian:
            return False
        
        # Always let AI learn during early exploration phase
        if self.n_games < self.min_exploration_games:
            return False
        
        # Calculate danger level
        danger = self.calculate_danger_level(game)
        
        # Use Hamiltonian if danger is high
        if danger >= (1.0 - self.danger_threshold):
            return True
        
        # Use Hamiltonian if safety score is low
        if self.hamiltonian:
            safety = self.hamiltonian.calculate_safety_score(game.head, game.snake)
            if safety < self.danger_threshold:
                return True
        
        # Check if snake is long (higher stakes, be more careful)
        if len(game.snake) > 20 and danger > 0.4:
            return True
        
        return False
    
    def get_action(self, game):
        """
        Get action using hybrid approach
        
        Returns:
            Action array [straight, right, left]
        """
        # Decide strategy
        use_ham = self.should_use_hamiltonian(game)
        
        if use_ham:
            # Use Hamiltonian cycle for safety with smart shortcuts to food
            self.hamiltonian_uses += 1
            action = self.hamiltonian.get_direction_to_next(
                game.head, game.direction, game.food, game.snake
            )
            return action
        
        # Use AI decision
        self.ai_decisions += 1
        state = self.get_state(game)
        
        # Improved exploration strategy
        self.epsilon = 80 - self.n_games
        final_moves = [0, 0, 0]
        
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
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_statistics(self):
        """Get usage statistics"""
        total = self.hamiltonian_uses + self.ai_decisions
        if total == 0:
            return "No decisions made yet"
        
        ham_percent = (self.hamiltonian_uses / total) * 100
        ai_percent = (self.ai_decisions / total) * 100
        
        return f"AI: {ai_percent:.1f}% | Hamiltonian: {ham_percent:.1f}%"


def train():
    """Training function with hybrid agent"""
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    
    # Create hybrid agent
    agent = HybridAgent(use_hamiltonian=True)
    game = SnakeGameAI()
    
    record = agent.record
    
    if agent.n_games > 0:
        print(f'Continuing from game {agent.n_games + 1}...\n')
    
    while True:
        # Get old state
        state_old = agent.get_state(game)
        
        # Get move (hybrid decision)
        final_move = agent.get_action(game)
        
        # Perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
        # Remember
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if done:
            # Train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            # Reset statistics for next game
            game_ham_uses = agent.hamiltonian_uses
            game_ai_decisions = agent.ai_decisions
            agent.hamiltonian_uses = 0
            agent.ai_decisions = 0
            
            # Update scores
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / len(plot_scores)
            plot_mean_scores.append(mean_score)
            
            # Save model
            if score > record:
                record = score
                agent.model.save(record=record, n_games=agent.n_games, mean_score=mean_score, folder=agent.model_folder)
                print(f'🎉 New Record! Score: {record}')
            else:
                if agent.n_games % 10 == 0:
                    agent.model.save(record=record, n_games=agent.n_games, mean_score=mean_score, folder=agent.model_folder)
            
            # Display statistics
            total_decisions = game_ham_uses + game_ai_decisions
            if total_decisions > 0:
                ai_pct = (game_ai_decisions / total_decisions) * 100
                ham_pct = (game_ham_uses / total_decisions) * 100
                print(f'Game {agent.n_games} | Score: {score} | Record: {record} | AI: {ai_pct:.0f}% Ham: {ham_pct:.0f}%')
            else:
                print(f'Game {agent.n_games} | Score: {score} | Record: {record}')
            
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
