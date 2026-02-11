# Contributing to AI Snake Game - Reinforcement Learning Agent

Thank you for your interest in contributing to the AI Snake Game - Reinforcement Learning Agent project! We welcome contributions from the community.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- Git installed and configured
- Basic understanding of Python and PyTorch
- Familiarity with reinforcement learning concepts (helpful but not required)

### Setting Up Your Development Environment

1. **Fork the repository**
   
   Click the "Fork" button at the top right of the repository page.

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-snake-game.git
   cd ai-snake-game
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, PyTorch version)
- Screenshots if applicable

### Suggesting Enhancements

We love new ideas! When suggesting enhancements:
- Use a clear, descriptive title
- Provide a detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include examples if possible

### Code Contributions

#### Types of Contributions We're Looking For

- 🐛 **Bug fixes**
- ✨ **New features** (reward systems, neural network architectures, etc.)
- 📚 **Documentation improvements**
- 🧪 **Additional test cases**
- 🎨 **UI/UX enhancements**
- ⚡ **Performance optimizations**
- 🔧 **Code refactoring**

#### Development Guidelines

1. **Code Style**
   - Follow PEP 8 style guidelines
   - Use meaningful variable and function names
   - Add comments for complex logic
   - Keep functions focused and modular

2. **Documentation**
   - Update README.md if you change functionality
   - Add docstrings to new functions and classes
   - Update relevant documentation in `/docs`

3. **Testing**
   - Test your changes thoroughly
   - Ensure existing tests still pass
   - Add new tests for new features
   - Run the test suite before submitting:
     ```bash
     python tests/integration_test.py
     python tests/test_hamiltonian.py
     ```

4. **Commits**
   - Write clear, concise commit messages
   - Use present tense ("Add feature" not "Added feature")
   - Reference issue numbers when applicable
   - Example: `Fix collision detection bug (#123)`

#### Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**
   - Ensure all tests pass
   - Test the game visually if UI is affected
   - Check for any unintended side effects

3. **Commit and push**
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Provide a clear title and description
   - Link any related issues
   - Wait for review

5. **Code Review**
   - Be responsive to feedback
   - Make requested changes promptly
   - Discuss if you disagree with suggestions
   - Be respectful and professional

## 🎯 Areas for Contribution

### High Priority

- [ ] Implement dueling DQN architecture
- [ ] Add prioritized experience replay
- [ ] Create web-based demo interface
- [ ] Improve training visualization
- [ ] Add multi-agent training support

### Medium Priority

- [ ] Implement convolutional neural network option
- [ ] Add tournament mode for comparing agents
- [ ] Create configurable game board sizes
- [ ] Improve documentation with more examples
- [ ] Add save/resume training functionality

### Good First Issues

- [ ] Add more unit tests
- [ ] Improve code comments
- [ ] Fix typos in documentation
- [ ] Add error handling
- [ ] Create additional reward system examples

## 📚 Resources

### Learning Resources

- **Reinforcement Learning**: [Sutton & Barto's Book](http://incompleteideas.net/book/the-book.html)
- **Deep Q-Learning**: [DeepMind's DQN Paper](https://www.nature.com/articles/nature14236)
- **PyTorch Tutorials**: [pytorch.org/tutorials](https://pytorch.org/tutorials/)
- **Pygame Documentation**: [pygame.org/docs](https://www.pygame.org/docs/)

### Project Documentation

- [REWARD_SYSTEM_EXPLAINED.md](docs/REWARD_SYSTEM_EXPLAINED.md) - Understanding reward systems
- [HAMILTONIAN_INTEGRATION.md](docs/HAMILTONIAN_INTEGRATION.md) - Hybrid agent architecture
- [QUICK_TUNE_GUIDE.md](docs/QUICK_TUNE_GUIDE.md) - Parameter tuning

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, education, socio-economic status
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behavior includes:**
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, trolling, or derogatory comments
- Personal or political attacks
- Publishing others' private information
- Any conduct inappropriate in a professional setting

## ❓ Questions?

If you have questions about contributing:
- Check existing issues and pull requests first
- Read the documentation in `/docs`
- Create a new issue with the "question" label
- Reach out via email (if available)

## 🙏 Recognition

Contributors will be:
- Listed in the project contributors
- Acknowledged in release notes
- Appreciated by the community! ⭐

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for making AI Snake Game - Reinforcement Learning Agent better! 🐍🎮**
