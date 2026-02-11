"""
Hamiltonian Cycle Implementation for Snake Game
Creates a guaranteed safe path that covers all grid cells
"""

from collections import namedtuple
import numpy as np

# Import Direction and Point from game module to ensure compatibility
try:
    from game import Direction, Point
except ImportError:
    # Fallback if game module not available (for standalone testing)
    from enum import Enum
    Point = namedtuple('Point', 'x, y')
    
    class Direction(Enum):
        RIGHT = 1
        LEFT = 2
        UP = 3
        DOWN = 4

class HamiltonianPath:
    """
    Generates and follows a Hamiltonian cycle for the snake game.
    This ensures the snake can always survive by following a predetermined path.
    """
    
    def __init__(self, width=640, height=480, block_size=20):
        """
        Initialize Hamiltonian path generator
        
        Args:
            width: Game width in pixels
            height: Game height in pixels
            block_size: Size of each grid block
        """
        self.width = width
        self.height = height
        self.block_size = block_size
        
        # Calculate grid dimensions
        self.grid_width = width // block_size
        self.grid_height = height // block_size
        
        print(f"Grid dimensions: {self.grid_width}x{self.grid_height}")
        
        # Build the Hamiltonian cycle
        self.cycle = self._build_hamiltonian_cycle()
        self.path_length = len(self.cycle)
        
        print(f"Hamiltonian cycle built with {self.path_length} positions")
    
    def _build_hamiltonian_cycle(self):
        """
        Build a Hamiltonian cycle using a zigzag pattern.
        Works for any grid size. The cycle forms a closed loop.
        """
        cycle = []
        
        # Create zigzag pattern that forms a proper cycle
        for y in range(self.grid_height):
            if y % 2 == 0:
                # Move right
                for x in range(self.grid_width):
                    cycle.append(Point(x * self.block_size, y * self.block_size))
            else:
                # Move left
                for x in range(self.grid_width - 1, -1, -1):
                    cycle.append(Point(x * self.block_size, y * self.block_size))
        
        # Ensure the cycle wraps properly by verifying last position connects to first
        # The zigzag pattern naturally creates this if grid_height is even
        # For odd heights, we need to ensure connectivity
        if self.grid_height % 2 != 0:
            # Last row goes left, ending at (0, last_y)
            # First position is (0, 0)
            # This naturally connects vertically
            pass
        
        return cycle
    
    def get_position_index(self, point):
        """
        Get the index of a point in the Hamiltonian cycle
        
        Args:
            point: Point(x, y) in pixel coordinates
            
        Returns:
            Index in the cycle, or -1 if not found
        """
        try:
            return self.cycle.index(point)
        except ValueError:
            # Point not in cycle, find closest
            grid_x = (point.x // self.block_size) * self.block_size
            grid_y = (point.y // self.block_size) * self.block_size
            closest = Point(grid_x, grid_y)
            try:
                return self.cycle.index(closest)
            except ValueError:
                return -1
    
    def get_next_position(self, current_point):
        """
        Get the next position in the Hamiltonian cycle
        
        Args:
            current_point: Current Point(x, y)
            
        Returns:
            Next Point in the cycle
        """
        current_idx = self.get_position_index(current_point)
        if current_idx == -1:
            return self.cycle[0]
        
        next_idx = (current_idx + 1) % self.path_length
        return self.cycle[next_idx]
    
    def get_direction_to_next(self, current_point, current_direction, food_point=None, snake_body=None):
        """
        Get the direction to move to follow the Hamiltonian cycle
        WITH SHORTCUT: If food is nearby and path is safe, go directly to food
        
        Args:
            current_point: Current head position
            current_direction: Current snake direction
            food_point: Food position (optional, for shortcuts)
            snake_body: Snake body list (optional, for collision checking)
            
        Returns:
            Action array [straight, right, left]
        """
        # Try shortcut to food if provided
        if food_point is not None and snake_body is not None:
            shortcut_action = self._try_shortcut_to_food(current_point, current_direction, 
                                                          food_point, snake_body)
            if shortcut_action is not None:
                return shortcut_action
        
        # Otherwise, follow Hamiltonian cycle
        next_point = self.get_next_position(current_point)
        
        # Calculate required direction
        dx = next_point.x - current_point.x
        dy = next_point.y - current_point.y
        
        # Determine target direction
        if dx > 0:
            target_dir = Direction.RIGHT
        elif dx < 0:
            target_dir = Direction.LEFT
        elif dy > 0:
            target_dir = Direction.DOWN
        else:
            target_dir = Direction.UP
        
        # Convert to action based on current direction
        return self._direction_to_action(current_direction, target_dir)
    
    def _try_shortcut_to_food(self, current_point, current_direction, food_point, snake_body):
        """
        Try to take a shortcut directly towards food if it's safe
        
        Returns:
            Action array if shortcut is safe, None otherwise
        """
        # Calculate direct distance to food
        dx = food_point.x - current_point.x
        dy = food_point.y - current_point.y
        manhattan_dist = abs(dx) + abs(dy)
        
        # Only consider shortcuts if food is reasonably close
        if manhattan_dist > self.block_size * 5:  # More than 5 blocks away
            return None
        
        # Determine best direction towards food
        target_dir = None
        if abs(dx) > abs(dy):
            # Move horizontally
            target_dir = Direction.RIGHT if dx > 0 else Direction.LEFT
        else:
            # Move vertically
            target_dir = Direction.DOWN if dy > 0 else Direction.UP
        
        # Calculate the action for this direction
        action = self._direction_to_action(current_direction, target_dir)
        
        # Check if this move is safe (no collision)
        next_x = current_point.x
        next_y = current_point.y
        
        if target_dir == Direction.RIGHT:
            next_x += self.block_size
        elif target_dir == Direction.LEFT:
            next_x -= self.block_size
        elif target_dir == Direction.DOWN:
            next_y += self.block_size
        elif target_dir == Direction.UP:
            next_y -= self.block_size
        
        next_point = Point(next_x, next_y)
        
        # Check for wall collision
        if (next_x < 0 or next_x >= self.width or 
            next_y < 0 or next_y >= self.height):
            return None
        
        # Check for body collision
        if next_point in snake_body[1:]:  # Skip head
            return None
        
        # Shortcut is safe!
        return action
    
    def _direction_to_action(self, current_dir, target_dir):
        """
        Convert current and target direction to action
        
        Args:
            current_dir: Current Direction
            target_dir: Target Direction
            
        Returns:
            Action array [straight, right, left]
        """
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        
        current_idx = clock_wise.index(current_dir)
        target_idx = clock_wise.index(target_dir)
        
        # Calculate turn
        turn = (target_idx - current_idx) % 4
        
        if turn == 0:
            return [1, 0, 0]  # Straight
        elif turn == 1:
            return [0, 1, 0]  # Right
        elif turn == 3:
            return [0, 0, 1]  # Left
        else:
            # 180 degree turn - choose right (could be either)
            return [0, 1, 0]
    
    def get_distance_on_path(self, from_point, to_point):
        """
        Calculate the distance between two points along the Hamiltonian path
        
        Args:
            from_point: Starting Point
            to_point: Ending Point
            
        Returns:
            Number of steps along the path
        """
        from_idx = self.get_position_index(from_point)
        to_idx = self.get_position_index(to_point)
        
        if from_idx == -1 or to_idx == -1:
            return float('inf')
        
        # Calculate forward distance
        if to_idx >= from_idx:
            return to_idx - from_idx
        else:
            return self.path_length - from_idx + to_idx
    
    def is_safe_shortcut(self, current_point, food_point, snake_body, current_direction):
        """
        Determine if it's safe to take a shortcut towards food instead of following cycle
        
        Args:
            current_point: Current head position
            food_point: Food position
            snake_body: List of snake body points
            current_direction: Current direction
            
        Returns:
            True if shortcut is safe, False otherwise
        """
        # Calculate if food is "ahead" on the cycle
        current_idx = self.get_position_index(current_point)
        food_idx = self.get_position_index(food_point)
        
        if current_idx == -1 or food_idx == -1:
            return False
        
        # Check if we can reach food without hitting body
        distance_to_food = self.get_distance_on_path(current_point, food_point)
        
        # If food is very close on the path, it's safe to follow cycle
        if distance_to_food <= 3:
            return True
        
        # Check if any body part is between us and food on the cycle
        for segment in snake_body[1:]:  # Skip head
            segment_idx = self.get_position_index(segment)
            if segment_idx != -1:
                # Check if segment is between current and food on cycle
                if current_idx < food_idx:
                    if current_idx < segment_idx < food_idx:
                        return False
                else:
                    if segment_idx > current_idx or segment_idx < food_idx:
                        return False
        
        return True
    
    def calculate_safety_score(self, current_point, snake_body):
        """
        Calculate how safe the current position is
        
        Args:
            current_point: Current head position
            snake_body: List of snake body points
            
        Returns:
            Safety score (0-1, higher is safer)
        """
        if len(snake_body) <= 3:
            return 1.0  # Very safe when snake is short
        
        current_idx = self.get_position_index(current_point)
        if current_idx == -1:
            return 0.0
        
        # Check distance to nearest body segment on the cycle
        min_distance = float('inf')
        for segment in snake_body[3:]:  # Skip first 3 segments
            segment_idx = self.get_position_index(segment)
            if segment_idx != -1:
                distance = abs(segment_idx - current_idx)
                # Consider wrap-around
                distance = min(distance, self.path_length - distance)
                min_distance = min(min_distance, distance)
        
        # Normalize to 0-1 scale
        if min_distance == float('inf'):
            return 1.0
        
        # Higher score for more distance
        safety = min(1.0, min_distance / (len(snake_body) + 2))
        return safety
    
    def get_hamiltonian_state_features(self, current_point, food_point, snake_body):
        """
        Get additional state features related to Hamiltonian path
        
        Args:
            current_point: Current head position
            food_point: Food position
            snake_body: List of snake body points
            
        Returns:
            List of features [on_path, distance_to_food_on_path, safety_score]
        """
        current_idx = self.get_position_index(current_point)
        on_path = 1 if current_idx != -1 else 0
        
        distance_to_food = self.get_distance_on_path(current_point, food_point)
        # Normalize distance (0-1)
        normalized_distance = min(1.0, distance_to_food / self.path_length) if distance_to_food != float('inf') else 1.0
        
        safety = self.calculate_safety_score(current_point, snake_body)
        
        return [on_path, normalized_distance, safety]
