import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import json
from datetime import datetime


class Linear_QNet(nn.Module):
    """Simple 2-layer Q-network."""
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        return self.fc2(F.relu(self.fc1(x)))

    def save(self, file_name='model.pth', record=0, n_games=0, mean_score=0.0, folder='./model'):
        os.makedirs(folder, exist_ok=True)
        torch.save(self.state_dict(), os.path.join(folder, file_name))
        with open(os.path.join(folder, 'metadata.json'), 'w') as f:
            json.dump({
                'record':     record,
                'n_games':    n_games,
                'mean_score': mean_score,
                'timestamp':  datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }, f, indent=4)
        print(f'Model saved | Record: {record} | Games: {n_games} | Mean: {mean_score:.2f}')

    def load(self, file_name='model.pth', folder='./model'):
        path = os.path.join(folder, file_name)
        if os.path.exists(path):
            self.load_state_dict(torch.load(path, weights_only=True))
            print(f'Model loaded from {path}')
            return True
        return False


class QTrainer:
    """Bellman-equation based Q-learning trainer."""
    def __init__(self, model, lr, gamma):
        self.gamma     = gamma
        self.model     = model
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state      = torch.tensor(state,      dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action     = torch.tensor(action,     dtype=torch.long)
        reward     = torch.tensor(reward,     dtype=torch.float)

        if len(state.shape) == 1:   # single sample → add batch dim
            state      = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action     = action.unsqueeze(0)
            reward     = reward.unsqueeze(0)
            done       = (done,)

        pred   = self.model(state)
        target = pred.clone()

        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
            target[i][torch.argmax(action[i]).item()] = Q_new

        self.optimizer.zero_grad()
        self.criterion(target, pred).backward()
        self.optimizer.step()