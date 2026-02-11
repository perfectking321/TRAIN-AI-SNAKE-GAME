"""
Visual Demonstration of Hybrid AI + Hamiltonian System
Shows when AI vs Hamiltonian is being used
"""

import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import SnakeGameAI, Direction, Point
from hamiltonian_path import HamiltonianPath
from agent_hybrid import HybridAgent

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

def visualize_hamiltonian_path(ham):
    """
    Visualize the Hamiltonian cycle on the grid
    """
    print("\n" + "="*60)
    print("HAMILTONIAN CYCLE VISUALIZATION")
    print("="*60)
    
    pygame.init()
    display = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Hamiltonian Cycle Visualization')
    font = pygame.font.Font('arial.ttf', 20)
    
    clock = pygame.time.Clock()
    
    print("Displaying Hamiltonian cycle...")
    print("Press SPACE to start animation")
    print("Press Q to quit")
    
    waiting = True
    animating = False
    current_idx = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    animating = True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
        
        display.fill(BLACK)
        
        if not waiting:
            # Draw the path with gradient colors
            for i in range(len(ham.cycle)):
                point = ham.cycle[i]
                
                # Color based on position in cycle
                ratio = i / len(ham.cycle)
                if i <= current_idx or not animating:
                    # Gradient from blue to purple
                    r = int(128 * ratio)
                    g = 0
                    b = int(255 * (1 - ratio))
                    color = (r, g, b)
                    
                    pygame.draw.rect(display, color, 
                                   pygame.Rect(point.x + 2, point.y + 2, 16, 16))
                
                # Draw connections
                if i < len(ham.cycle) - 1 and (i < current_idx or not animating):
                    next_point = ham.cycle[i + 1]
                    pygame.draw.line(display, (100, 100, 100), 
                                   (point.x + 10, point.y + 10),
                                   (next_point.x + 10, next_point.y + 10), 2)
            
            # Draw current position if animating
            if animating and current_idx < len(ham.cycle):
                current = ham.cycle[current_idx]
                pygame.draw.rect(display, YELLOW,
                               pygame.Rect(current.x, current.y, 20, 20))
                pygame.draw.rect(display, ORANGE,
                               pygame.Rect(current.x + 4, current.y + 4, 12, 12))
        
        # Display info
        if waiting:
            text = font.render("Press SPACE to animate", True, WHITE)
            display.blit(text, [150, 230])
        else:
            text = font.render(f"Position: {current_idx}/{len(ham.cycle)}", True, WHITE)
            display.blit(text, [10, 10])
            
            if animating:
                current_idx += 1
                if current_idx >= len(ham.cycle):
                    animating = False
                    current_idx = 0
        
        pygame.display.flip()
        clock.tick(30)  # 30 FPS


def demo_hybrid_game():
    """
    Demonstrate hybrid AI playing the game
    Shows when using AI vs Hamiltonian
    """
    print("\n" + "="*60)
    print("HYBRID AI DEMONSTRATION")
    print("="*60)
    
    pygame.init()
    font = pygame.font.Font('arial.ttf', 16)
    
    # Create hybrid agent and game
    agent = HybridAgent(use_hamiltonian=True)
    game = SnakeGameAI()
    
    # Override display to show additional info
    display = game.display
    
    print("\nRunning hybrid AI demonstration...")
    print("Green snake = AI decision")
    print("Purple snake = Hamiltonian safety mode")
    print("Press Q to quit, SPACE to pause")
    
    running = True
    paused = False
    game_count = 0
    
    while running and game_count < 3:  # Run 3 games
        # Get action
        use_ham = agent.should_use_hamiltonian(game)
        final_move = agent.get_action(game)
        
        # Perform move
        reward, done, score = game.play_step(final_move)
        
        # Custom rendering
        display.fill(BLACK)
        
        # Draw snake with color based on mode
        snake_color1 = PURPLE if use_ham else GREEN
        snake_color2 = (160, 0, 160) if use_ham else (0, 160, 0)
        
        for pt in game.snake:
            pygame.draw.rect(display, snake_color1, 
                           pygame.Rect(pt.x, pt.y, 20, 20))
            pygame.draw.rect(display, snake_color2, 
                           pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        
        # Draw food
        pygame.draw.rect(display, RED, 
                        pygame.Rect(game.food.x, game.food.y, 20, 20))
        
        # Display info
        score_text = font.render(f"Score: {score}", True, WHITE)
        display.blit(score_text, [10, 10])
        
        mode_text = font.render(
            f"Mode: {'HAMILTONIAN' if use_ham else 'AI LEARNING'}", 
            True, PURPLE if use_ham else GREEN
        )
        display.blit(mode_text, [10, 35])
        
        danger = agent.calculate_danger_level(game)
        danger_text = font.render(f"Danger: {danger*100:.0f}%", True, 
                                 RED if danger > 0.7 else WHITE)
        display.blit(danger_text, [10, 60])
        
        game_text = font.render(f"Game: {game_count + 1}/3", True, WHITE)
        display.blit(game_text, [10, 85])
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused
        
        if paused:
            continue
        
        if done:
            print(f"Game {game_count + 1} completed. Score: {score}")
            game_count += 1
            if game_count < 3:
                game.reset()
    
    pygame.quit()
    print("\nDemonstration completed!")


def main():
    """Main demo function"""
    print("\n" + "#"*60)
    print("# HAMILTONIAN HYBRID SYSTEM DEMONSTRATION")
    print("#"*60)
    print("\nChoose demonstration:")
    print("1. Visualize Hamiltonian Cycle")
    print("2. Watch Hybrid AI Play (3 games)")
    print("3. Both")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    ham = HamiltonianPath(640, 480, 20)
    
    if choice == '1':
        visualize_hamiltonian_path(ham)
    elif choice == '2':
        demo_hybrid_game()
    elif choice == '3':
        visualize_hamiltonian_path(ham)
        demo_hybrid_game()
    else:
        print("Exiting...")
    
    print("\nThank you!")


if __name__ == "__main__":
    main()
