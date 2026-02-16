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
python -c "import torch; import pygame; import numpy; import matplotlib; import IPython" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully!"
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
