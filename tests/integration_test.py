"""
Integration Test - Test hybrid agent in headless mode
"""

import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Run pygame in headless mode

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import SnakeGameAI
from src.agent_hybrid import HybridAgent

def test_hybrid_agent_basic():
    """Test basic hybrid agent functionality"""
    print("\n" + "="*60)
    print("INTEGRATION TEST: Hybrid Agent")
    print("="*60)
    
    print("\nInitializing hybrid agent...")
    agent = HybridAgent(use_hamiltonian=True)
    
    print("✓ Agent created successfully")
    print(f"  State size: 14 features (11 original + 3 Hamiltonian)")
    print(f"  Model: Linear_QNet with 256 hidden units")
    
    # Test state generation
    print("\nTesting state generation...")
    game = SnakeGameAI()
    state = agent.get_state(game)
    
    print(f"✓ State generated: {len(state)} features")
    print(f"  State values: {state}")
    
    assert len(state) == 14, f"Expected 14 features, got {len(state)}"
    print("✓ State size correct")
    
    # Test action generation
    print("\nTesting action generation...")
    action = agent.get_action(game)
    
    print(f"✓ Action generated: {action}")
    assert sum(action) == 1, f"Action should have exactly 1 active, got sum={sum(action)}"
    assert len(action) == 3, f"Action should have 3 elements, got {len(action)}"
    print("✓ Action format correct")
    
    # Test danger calculation
    print("\nTesting danger calculation...")
    danger = agent.calculate_danger_level(game)
    print(f"✓ Danger level: {danger:.2f}")
    assert 0 <= danger <= 1, f"Danger should be 0-1, got {danger}"
    print("✓ Danger level in valid range")
    
    # Test Hamiltonian decision
    print("\nTesting Hamiltonian decision logic...")
    should_use = agent.should_use_hamiltonian(game)
    print(f"✓ Should use Hamiltonian: {should_use}")
    print(f"  (Early exploration: game {agent.n_games} < {agent.min_exploration_games})")
    
    return True


def test_hybrid_gameplay():
    """Test hybrid agent playing a few moves"""
    print("\n" + "="*60)
    print("INTEGRATION TEST: Hybrid Gameplay")
    print("="*60)
    
    print("\nRunning short gameplay test (100 moves)...")
    
    agent = HybridAgent(use_hamiltonian=True)
    game = SnakeGameAI()
    
    ai_count = 0
    ham_count = 0
    
    for move_num in range(100):
        use_ham = agent.should_use_hamiltonian(game)
        if use_ham:
            ham_count += 1
        else:
            ai_count += 1
        
        action = agent.get_action(game)
        reward, done, score = game.play_step(action)
        
        if done:
            print(f"✓ Game ended at move {move_num + 1}, score: {score}")
            break
    
    print(f"\nDecision statistics:")
    print(f"  AI decisions: {ai_count}")
    print(f"  Hamiltonian decisions: {ham_count}")
    total = ai_count + ham_count
    if total > 0:
        print(f"  AI percentage: {ai_count/total*100:.1f}%")
        print(f"  Hamiltonian percentage: {ham_count/total*100:.1f}%")
    
    print("✓ Gameplay test completed")
    return True


def test_comparison():
    """Quick comparison test"""
    print("\n" + "="*60)
    print("INTEGRATION TEST: Quick Comparison")
    print("="*60)
    
    print("\nTesting 3 games with hybrid agent...")
    
    agent = HybridAgent(use_hamiltonian=True)
    scores = []
    
    for game_num in range(3):
        game = SnakeGameAI()
        
        while True:
            action = agent.get_action(game)
            reward, done, score = game.play_step(action)
            
            if done:
                scores.append(score)
                print(f"  Game {game_num + 1}: Score = {score}")
                break
    
    avg_score = sum(scores) / len(scores)
    print(f"\n✓ Average score: {avg_score:.1f}")
    print(f"  Min: {min(scores)}, Max: {max(scores)}")
    
    return True


def run_integration_tests():
    """Run all integration tests"""
    print("\n" + "#"*60)
    print("# HAMILTONIAN INTEGRATION TESTS")
    print("#"*60)
    
    tests = [
        ("Basic Functionality", test_hybrid_agent_basic),
        ("Hybrid Gameplay", test_hybrid_gameplay),
        ("Quick Comparison", test_comparison),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"Running: {name}")
            print('='*60)
            
            result = test_func()
            if result:
                passed += 1
                print(f"✓ {name} PASSED")
            else:
                failed += 1
                print(f"✗ {name} FAILED")
        except Exception as e:
            print(f"\n✗ {name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Final report
    print("\n" + "#"*60)
    print("# INTEGRATION TEST RESULTS")
    print("#"*60)
    print(f"Total Tests: {len(tests)}")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL INTEGRATION TESTS PASSED! 🎉")
        print("\nYour Hamiltonian integration is ready to use!")
        print("\nNext steps:")
        print("  - Run: python agent_hybrid.py  (train hybrid agent)")
        print("  - Run: python demo_hybrid.py   (visual demo)")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    print("#"*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
