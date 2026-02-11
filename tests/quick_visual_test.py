""" 
Quick Visual Test - Shows Hamiltonian cycle path
No pygame window needed - ASCII visualization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.hamiltonian_path import HamiltonianPath, Point, Direction

def visualize_path_ascii():
    """Visualize first few steps of Hamiltonian path in ASCII"""
    print("\n" + "="*60)
    print("HAMILTONIAN CYCLE VISUALIZATION (ASCII)")
    print("="*60)
    
    ham = HamiltonianPath(640, 480, 20)
    
    # Show first 100 positions
    print("\nFirst 100 positions in the cycle:")
    print("(Each row shows 10 positions)\n")
    
    for i in range(0, min(100, len(ham.cycle)), 10):
        positions = ham.cycle[i:i+10]
        pos_strs = [f"({p.x:3},{p.y:3})" for p in positions]
        print(f"[{i:3d}-{i+9:3d}]: " + " ".join(pos_strs))
    
    print(f"\n... ({len(ham.cycle) - 100} more positions)")
    
    # Show last 10 positions
    print("\nLast 10 positions:")
    for i in range(len(ham.cycle) - 10, len(ham.cycle)):
        p = ham.cycle[i]
        print(f"[{i:3d}]: ({p.x:3},{p.y:3})")
    
    print("\nCycle info:")
    print(f"  Total positions: {len(ham.cycle)}")
    print(f"  Grid: {ham.grid_width}x{ham.grid_height}")
    print(f"  Starts at: {ham.cycle[0]}")
    print(f"  Ends at: {ham.cycle[-1]}")
    next_pos = ham.get_next_position(ham.cycle[-1])
    print(f"  Next after end: {next_pos} (wraps to start)")


def test_pathfinding():
    """Test pathfinding capabilities"""
    print("\n" + "="*60)
    print("PATHFINDING TEST")
    print("="*60)
    
    ham = HamiltonianPath(640, 480, 20)
    
    # Test cases
    test_cases = [
        (Point(0, 0), Point(100, 100)),
        (Point(200, 200), Point(400, 400)),
        (Point(600, 400), Point(20, 20)),
    ]
    
    for start, end in test_cases:
        distance = ham.get_distance_on_path(start, end)
        start_idx = ham.get_position_index(start)
        end_idx = ham.get_position_index(end)
        
        print(f"\nFrom {start} to {end}:")
        print(f"  Start index: {start_idx}")
        print(f"  End index: {end_idx}")
        print(f"  Distance: {distance} steps")


def test_safety_features():
    """Test safety calculations"""
    print("\n" + "="*60)
    print("SAFETY FEATURES TEST")
    print("="*60)
    
    ham = HamiltonianPath(640, 480, 20)
    
    # Test with different snake lengths
    print("\nSafety scores for different snake lengths:")
    
    test_snakes = [
        ([Point(100, 100), Point(80, 100), Point(60, 100)], "Short snake (3)"),
        ([Point(x * 20, 0) for x in range(10)], "Medium snake (10)"),
        ([Point(x * 20, 0) for x in range(20)], "Long snake (20)"),
    ]
    
    for snake, desc in test_snakes:
        head = snake[0]
        food = Point(300, 300)
        
        safety = ham.calculate_safety_score(head, snake)
        features = ham.get_hamiltonian_state_features(head, food, snake)
        
        print(f"\n{desc}:")
        print(f"  Head at: {head}")
        print(f"  Safety score: {safety:.2f}")
        print(f"  Features: on_path={features[0]}, dist={features[1]:.2f}, safety={features[2]:.2f}")


def main():
    """Run all quick tests"""
    print("\n" + "#"*60)
    print("# HAMILTONIAN QUICK VISUAL TEST")
    print("#"*60)
    
    visualize_path_ascii()
    test_pathfinding()
    test_safety_features()
    
    print("\n" + "#"*60)
    print("# Tests Complete!")
    print("#"*60)
    print("\nNext steps:")
    print("  1. Run full test suite: python test_hamiltonian.py")
    print("  2. Try visual demo: python demo_hybrid.py")
    print("  3. Train hybrid AI: python agent_hybrid.py")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
