import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import json
from datetime import datetime

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth', record=0, n_games=0, mean_score=0.0, folder='./model'):
        """Save model with metadata"""
        model_folder_path = folder
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        # Save the best model
        best_model_path = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), best_model_path)
        
        # Save metadata
        metadata = {
            'record': record,
            'n_games': n_games,
            'mean_score': mean_score,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        metadata_path = os.path.join(model_folder_path, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        # Save a timestamped checkpoint
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_name = f'checkpoint_{timestamp}_score{record}.pth'
        checkpoint_path = os.path.join(model_folder_path, checkpoint_name)
        torch.save(self.state_dict(), checkpoint_path)
        
        print(f'Model saved! Record: {record}, Games: {n_games}, Mean Score: {mean_score:.2f}')
    
    def load(self, file_name='model.pth', folder='./model'):
        """Load model weights"""
        model_folder_path = folder
        file_path = os.path.join(model_folder_path, file_name)
        
        if os.path.exists(file_path):
            self.load_state_dict(torch.load(file_path))
            print(f'Model loaded from {file_path}')
            return True
        return False

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state ,action ,reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        #(n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        #1: predicted Q value with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # FIXED: Use action[idx] to get the correct action for this sample
            target[idx][torch.argmax(action[idx]).item()] = Q_new
            
        #2: Q_new = r + gamma * max(next_predicted Q value)
        # Update only the Q-value for the action that was taken
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()