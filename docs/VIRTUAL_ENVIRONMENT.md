# Virtual Environment Setup Guide

This guide explains how to use the virtual environment (venv) for the AI Snake Game project.

## What is a Virtual Environment?

A virtual environment is an isolated Python environment that keeps dependencies required by this project separate from your system-wide Python packages. This prevents version conflicts and makes the project easier to manage.

## Quick Setup

### Automated Setup (Recommended)

The easiest way to set up the environment is using the provided setup script:

```bash
./setup.sh
```

This script will:
- Create a virtual environment in the `venv/` directory
- Upgrade pip to the latest version
- Install all required dependencies from `requirements.txt`
- Verify the installation

### Manual Setup

If you prefer manual setup or the script doesn't work on your system:

#### 1. Create the virtual environment

```bash
python3 -m venv venv
```

#### 2. Activate the virtual environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

You'll know it's activated when you see `(venv)` at the beginning of your terminal prompt.

#### 3. Upgrade pip

```bash
pip install --upgrade pip
```

#### 4. Install dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **torch** - PyTorch for deep learning
- **pygame** - For the game environment
- **numpy** - For numerical computations
- **matplotlib** - For plotting training progress
- **ipython** - Enhanced Python shell (optional)

## Using the Virtual Environment

### Activating the Environment

You need to activate the virtual environment every time you open a new terminal session:

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### Running the Project

Once activated, you can run any of the project scripts:

```bash
# Train the standard DQN agent
python train.py

# Train the hybrid agent
python train_hybrid.py

# Watch the AI play
python demo.py

# Run tests
python tests/integration_test.py
```

### Deactivating the Environment

When you're done working on the project:

```bash
deactivate
```

## Verifying Installation

To check that all dependencies are installed correctly:

```bash
# Activate the environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Check installed packages
pip list

# Test imports
python -c "import torch, pygame, numpy, matplotlib, IPython; print('✅ All dependencies working!')"
```

## Troubleshooting

### "venv not found" error

Make sure you're in the project root directory:
```bash
cd /path/to/AI-Snake-Game--Reinforcement-Learning-Agent
```

### Python version issues

This project requires Python 3.7 or higher. Check your version:
```bash
python3 --version
```

### PyTorch installation issues

PyTorch is a large package and may take several minutes to download. If installation fails:

1. Check your internet connection
2. Try installing PyTorch separately first:
   ```bash
   pip install torch
   ```
3. Then install the rest:
   ```bash
   pip install -r requirements.txt
   ```

### Permission errors on Linux/macOS

If you get permission errors when running `setup.sh`:
```bash
chmod +x setup.sh
./setup.sh
```

## Managing Dependencies

### Adding new dependencies

1. Activate the virtual environment
2. Install the package:
   ```bash
   pip install package-name
   ```
3. Update requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```

### Updating dependencies

To update all dependencies to their latest versions:
```bash
pip install --upgrade -r requirements.txt
```

## Why Use a Virtual Environment?

✅ **Isolation** - Dependencies don't interfere with other Python projects  
✅ **Reproducibility** - Everyone working on the project uses the same versions  
✅ **Clean system** - No need to install packages system-wide  
✅ **Easy cleanup** - Just delete the `venv/` folder to remove everything  

## Additional Resources

- [Python venv documentation](https://docs.python.org/3/library/venv.html)
- [PyTorch installation guide](https://pytorch.org/get-started/locally/)
- [Pygame documentation](https://www.pygame.org/docs/)

---

For more information about the project itself, see the main [README.md](../README.md).
