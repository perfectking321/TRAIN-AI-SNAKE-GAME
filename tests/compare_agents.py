"""
Compare Performance: Pure AI vs Hybrid AI
Run side-by-side comparison
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import SnakeGameAI

# Import both agents
from src.agent import Agent as PureAgent
from src.agent_hybrid import HybridAgent

def run_comparison_test(num_games=10):
    """
    Run comparison test between pure AI and hybrid AI
    
    Args:
        num_games: Number of games to test each agent
    """
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON TEST")
    print("="*60)
    print(f"Running {num_games} games for each agent...\n")
    
    # Test Pure AI
    print("Testing Pure AI Agent...")
    pure_scores = []
    
    try:
        pure_agent = PureAgent()
    except RuntimeError as e:
        if "size mismatch" in str(e):
            print("⚠️  Warning: Saved model incompatible with Pure AI (size mismatch)")
            print("Creating fresh Pure AI agent...\n")
            # Create new pure agent without loading old model
            pure_agent = PureAgent()
            pure_agent.record = 0  # Reset record
        else:
            raise
    
    for i in range(num_games):
        game = SnakeGameAI()
        score = 0
        
        while True:
            state = pure_agent.get_state(game)
            action = pure_agent.get_action(state)
            reward, done, score = game.play_step(action)
            
            if done:
                pure_scores.append(score)
                print(f"  Game {i+1}: Score = {score}")
                break
    
    # Test Hybrid AI
    print("\nTesting Hybrid AI Agent...")
    hybrid_scores = []
    hybrid_agent = HybridAgent(use_hamiltonian=True)
    
    for i in range(num_games):
        game = SnakeGameAI()
        score = 0
        
        while True:
            action = hybrid_agent.get_action(game)
            reward, done, score = game.play_step(action)
            
            if done:
                hybrid_scores.append(score)
                print(f"  Game {i+1}: Score = {score}")
                break
    
    # Calculate statistics
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    pure_avg = sum(pure_scores) / len(pure_scores)
    pure_max = max(pure_scores)
    pure_min = min(pure_scores)
    
    hybrid_avg = sum(hybrid_scores) / len(hybrid_scores)
    hybrid_max = max(hybrid_scores)
    hybrid_min = min(hybrid_scores)
    
    print(f"\nPure AI Agent:")
    print(f"  Average Score: {pure_avg:.2f}")
    print(f"  Max Score: {pure_max}")
    print(f"  Min Score: {pure_min}")
    print(f"  Scores: {pure_scores}")
    
    print(f"\nHybrid AI Agent:")
    print(f"  Average Score: {hybrid_avg:.2f}")
    print(f"  Max Score: {hybrid_max}")
    print(f"  Min Score: {hybrid_min}")
    print(f"  Scores: {hybrid_scores}")
    
    print(f"\nImprovement:")
    improvement = ((hybrid_avg - pure_avg) / pure_avg * 100) if pure_avg > 0 else 0
    print(f"  Average: {improvement:+.1f}%")
    print(f"  Max: {hybrid_max - pure_max:+d}")
    
    if hybrid_avg > pure_avg:
        print("\n✓ Hybrid AI performed better on average!")
    elif hybrid_avg < pure_avg:
        print("\n⚠ Pure AI performed better on average")
    else:
        print("\n= Both agents performed equally")
    
    print("="*60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare Pure AI vs Hybrid AI')
    parser.add_argument('--games', type=int, default=10, 
                       help='Number of games to test (default: 10)')
    
    args = parser.parse_args()
    
    run_comparison_test(args.games)
