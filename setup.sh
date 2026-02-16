#!/bin/bash
# Setup script for AI Snake Game - Reinforcement Learning Agent
# This script creates a virtual environment and installs all dependencies

echo "🐍 Setting up AI Snake Game environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Verify installation
echo "🔍 Verifying installation..."
if ! python -c "import torch" 2>/dev/null; then
    echo "❌ Failed to import torch"
    exit 1
fi

if ! python -c "import pygame" 2>/dev/null; then
    echo "❌ Failed to import pygame"
    exit 1
fi

if ! python -c "import numpy" 2>/dev/null; then
    echo "❌ Failed to import numpy"
    exit 1
fi

if ! python -c "import matplotlib" 2>/dev/null; then
    echo "❌ Failed to import matplotlib"
    exit 1
fi

if ! python -c "import IPython" 2>/dev/null; then
    echo "⚠️  Warning: IPython not installed (optional dependency)"
fi

echo "✅ All core dependencies installed successfully!"
    echo ""
    echo "To activate the virtual environment, run:"
    echo "  source venv/bin/activate"
    echo ""
    echo "To train the model, run:"
    echo "  python train.py"
    echo ""
    echo "To run the demo, run:"
    echo "  python demo.py"
else
    echo "❌ Some dependencies failed to install. Please check the error messages above."
    exit 1
fi
