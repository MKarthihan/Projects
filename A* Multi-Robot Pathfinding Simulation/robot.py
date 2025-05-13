import copy
from a_star import a_star, heuristic
import communication  # Assumed to implement broadcast_obstacle_data() and receive_obstacle_data()
from utils import manhattan_distance, euclidean_distance

class Robot:
    """
    Represents a robot in the multi-agent path planning simulation.
    
    Attributes:
        id (int): Unique identifier for the robot.
        position (tuple): Current (x, y) coordinate.
        environment (Environment): Global simulation environment.
        local_grid (list): Local copy of the environment grid for dynamic obstacle updates.
        path (list): Planned path as a list of (x, y) coordinates.
    """
    
    def __init__(self, robot_id, start_pos, environment):
        """
        Initialize the robot with its ID, starting position, and environment.
        
        Args:
            robot_id (int): Unique robot identifier.
            start_pos (tuple): Starting (x, y) position.
            environment (Environment): The simulation environment.
        """
        self.id = robot_id
        self.position = start_pos
        self.environment = environment
        #create a deep copy of the global grid to allow local updates.
        self.local_grid = [row[:] for row in environment.grid]
        self.path = []
        self.finished = False
        self.steps_taken = 0
        self.replans = 0
        self.obstacles_shared = 0
        self.obstacles_received = 0
        self.full_path = []
        self.trace_path = [start_pos]
        self.ready_to_move = False

    def plan_path(self, heuristic_method="Manhattan"):
        """
        Plans an optimal path from the robot's current position to the rendezvous point using A*.
        
        Args:
            heuristic_method (str): Heuristic type ("Manhattan" or "Euclidean").
            
        Returns:
            list: The computed path as a list of (x, y) coordinates, or None if no path is found.
        """
        if self.finished:
            return self.path

        self.replans += 1

        if heuristic_method == "Manhattan":
            from utils import manhattan_distance as h_func
        else:
            from utils import euclidean_distance as h_func

        self.path = a_star(self.position, self.environment.rendezvous_point, self.local_grid, h_func)
        self.ready_to_move = all(
            0 <= pos[0] < self.environment.dimensions[1] and
            0 <= pos[1] < self.environment.dimensions[0] and
            self.local_grid[pos[1]][pos[0]] == 0
            for pos in self.path
        )
        self.full_path = self.path.copy() if self.path else []
        return self.path

    def move(self):
        # print("robot tried to move")
        """
        Moves the robot one step along its planned path.
        If the next step is invalid (due to a new obstacle), the robot re-plans its path.
        
        Returns:
            bool: True if the robot moved successfully, False otherwise.
        """
        if not self.path or len(self.path) < 2:
            return False

        next_step = self.path[1]

        if next_step == self.environment.rendezvous_point:
            self.position = next_step
            self.trace_path.append(self.position)
            self.path.pop(0)
            self.finished = True
            self.steps_taken += 1
            return True

        if self.environment.is_valid_position(next_step):
            self.position = next_step
            self.path.pop(0)
            self.steps_taken += 1
            self.trace_path.append(self.position)
            return True
        else:
            self.path.pop(0)  # remove invalid move
            self.plan_path()
            return False

    def update_map(self, shared_obstacles):
        """
        Updates the robot's local grid with new obstacle data shared by other robots.
        
        Args:
            shared_obstacles (iterable): An iterable of (x, y) obstacle positions.
        """
        for obs in shared_obstacles:
            x, y = obs
            rows, cols = self.environment.dimensions
            if 0 <= x < cols and 0 <= y < rows:
                self.local_grid[y][x] = 1  #obstacle

    def communicate(self):
        """
        Shares newly detected obstacles with other robots.
        This simulates checking adjacent cells and broadcasting any new obstacle.
        """
        detected_obstacles = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        rows, cols = self.environment.dimensions

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                env_val = self.environment.grid[ny][nx]
                if self.local_grid[ny][nx] != env_val:
                    detected_obstacles.append((nx, ny))

        if detected_obstacles:
            self.obstacles_shared += len(detected_obstacles)
            communication.broadcast_obstacle_data(self.id, detected_obstacles)

    def receive_communications(self):
        """
        Receives obstacle data shared by other robots and updates the local map.
        """
        shared_data = communication.receive_obstacle_data(self.id)
        if shared_data:
            self.obstacles_received += len(shared_data)
            self.update_map(shared_data)
            print(f"Robot {self.id} updated map with: {shared_data}")
