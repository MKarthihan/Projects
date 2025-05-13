import os

class Environment:
    def __init__(self, dimensions, obstacles, rendezvous_point, robot_positions, grid):
        """
        Initialize the environment with its dimensions, obstacles, rendezvous point,
        robot positions, and grid representation.
        
        Args:
            dimensions (tuple): A tuple (rows, cols) for the grid dimensions.
            obstacles (set): Set of (x, y) positions that are blocked.
            rendezvous_point (tuple): (x, y) coordinate of the target.
            robot_positions (list): List of (x, y) coordinates for each robot.
            grid (list): 2D list representing the grid (each cell is 0 or 1).
        """
        self.dimensions = dimensions  # (rows, cols)
        self.obstacles = obstacles
        self.rendezvous_point = rendezvous_point
        self.robot_positions = robot_positions
        self.grid = grid

    @classmethod
    def read_from_file(cls, file_path):
        """
        Reads the environment configuration from a text file and creates an Environment instance.
        
        The expected file format is:
            <rows> <cols>
            <number_of_robots>
            <robot1_x> <robot1_y>
            <robot2_x> <robot2_y>
            ...
            <rendezvous_x> <rendezvous_y>
            <grid_row_1>
            <grid_row_2>
            ...
            <grid_row_n>
        
        Note: The grid rows are provided starting from the top row.
        
        Args:
            file_path (str): Path to the input text file (assumed in same folder as the .py file).
            
        Returns:
            Environment: An instance of the Environment class.
        """
        with open(file_path, "r") as file:
            lines = []
            for line in file:
                #remove any inline comments (anything after "//") and strip whitespace
                line = line.split("//")[0].strip()
                if line:
                    lines.append(line)
        
        # grid dimensions (first line)
        dims = lines[0].split()
        rows, cols = int(dims[0]), int(dims[1])
        dimensions = (rows, cols)
        
        #number of robots (second line)
        num_robots = int(lines[1])
        robot_positions = []
        for i in range(num_robots):
            pos = lines[2 + i].split()
            x, y = int(pos[0]), int(pos[1])
            robot_positions.append((x, y))
        
        #rendezvous point (next line)
        rendezvous_line = lines[2 + num_robots].split()
        rendezvous_point = (int(rendezvous_line[0]), int(rendezvous_line[1]))
        
        #grid rows
        grid_lines = lines[3 + num_robots:]
        if len(grid_lines) != rows:
            raise ValueError("The number of grid rows does not match the specified dimension.")
        
        grid = []
        obstacles = set()
        # The file grid is given from top (highest y) to bottom (lowest y), first grid line corresponds to y = rows - 1
        for y, line in enumerate(grid_lines):
            grid_row = []
            for x, char in enumerate(line):
                cell = int(char)
                grid_row.append(cell)
                if cell == 1:
                    obstacles.add((x, y))
            grid.append(grid_row)

        return cls(dimensions, obstacles, rendezvous_point, robot_positions, grid)
    
    def is_valid_position(self, pos):
        """
        Checks if a given position is within the grid bounds and not occupied by an obstacle.
        
        Args:
            pos (tuple): (x, y) coordinate to check.
            
        Returns:
            bool: True if position is valid, False otherwise.
        """
        x, y = pos
        rows, cols = self.dimensions
        #check if position is within grid boundaries
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return False
        #check if the position is occupied by an obstacle
        if pos in self.obstacles:
            return False
        return True