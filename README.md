# 🐍 AI Snake Game

Train an AI to play Snake using Deep Q-Learning (DQN) with PyTorch. I built this to learn reinforcement learning and ended up creating a hybrid system that combines neural networks with Hamiltonian cycles for better performance.

## 🎯 What It Does

- Trains an AI agent to play Snake using Deep Q-Learning
- Has a "hybrid mode" that switches to a safe Hamiltonian path when things get dangerous
- Shows live training progress with plots and stats
- Saves the best models automatically
- Lets you watch the AI play with visual indicators

The AI learns from rewards (eating food = good, dying = bad) and gets pretty decent after 200+ games. Best scores I've seen are 60+ for standard mode and even higher with the hybrid approach.

## 📦 How to Run It

Clone the repo:
```bash
git clone https://github.com/yourusername/ai-snake-game.git
cd ai-snake-game
```

Install dependencies (option 1 - automated setup):
```bash
./setup.sh
```

Or install manually (option 2):
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

Start training:
```bash
# Standard DQN agent
python train.py

# Hybrid agent (DQN + Hamiltonian safety net)
python train_hybrid.py
```

Watch it play:
```bash
python demo.py
```

## 🧠 How It Works

The AI observes 11 things about the game state (danger ahead, food direction, etc.) and decides whether to go straight, turn left, or turn right. It learns through trial and error using Q-Learning.

**Reward System:**
- Eat food: +10
- Move toward food: +1
- Move away: -1
- Die: -10

**Hybrid Mode:**
When the AI detects it's in danger (safety < 30%), it switches to a Hamiltonian cycle path that guarantees survival. You'll see a yellow border when this happens. Green border = AI is in control.

## 📁 Project Structure

```
├── src/                   # Source code
│   ├── agent.py           # Standard DQN agent
│   ├── agent_hybrid.py    # Hybrid DQN + Hamiltonian
│   ├── game.py            # Snake game environment
│   ├── model.py           # Neural network (PyTorch)
│   ├── hamiltonian_path.py # Safety fallback path
│   ├── helper.py          # Plotting utilities
│   └── demo_hybrid.py     # Interactive demo
├── train.py               # Train standard agent
├── train_hybrid.py        # Train hybrid agent
├── demo.py                # Watch the AI play
├── tests/                 # Test scripts
├── docs/                  # Detailed documentation
├── assets/                # Fonts and resources
└── model/                src/ # Saved checkpoints
```

## 🔧 Configuration

**Adjust game speed** in `game.py`:
```python
SPEED = 5000  # Higher = slower
```

**Tune learning** - see [docs/QUICK_TUNE_GUIDE.md](docs/QUICK_TUNE_GUIDE.md)

**More docs** in `/docs`:
- Reward system explained
- Hamiltonian integration details
- Performance tuning tips

## 🧪 Testing

```bash
python tests/integration_test.py
python tests/test_hamiltonian.py
python tests/compare_agents.py
```

## 🤔 Why I Made This

I wanted to learn reinforcement learning and figured Snake was a perfect starting point. The hybrid approach came later when I realized the AI sometimes gets stuck in dangerous situations it can't learn its way out of.

## 🚧 Future Ideas

- Try different neural network architectures (CNN, Dueling DQN)
- Add prioritized experience replay
- Web-based demo
- Multi-agent training
- Configurable board sizes

## 💡 Contributing

Feel free to fork it and experiment! If you come up with better reward strategies or improvements, open a PR. Check [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

Built with Python, PyTorch, and Pygame
