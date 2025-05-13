import math

def manhattan_distance(pos1, pos2):
    """
    Computes the Manhattan distance between two positions.
    
    Args:
        pos1 (tuple): (x, y) coordinates of the first point.
        pos2 (tuple): (x, y) coordinates of the second point.
    
    Returns:
        int: The Manhattan distance.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_distance(pos1, pos2):
    """
    Computes the Euclidean distance between two positions.
    
    Args:
        pos1 (tuple): (x, y) coordinates of the first point.
        pos2 (tuple): (x, y) coordinates of the second point.
    
    Returns:
        float: The Euclidean distance.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def parse_input_file(file_path):
    """
    Parses an input file for the environment configuration.
    
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
    
    Grid rows are provided from top to bottom.
    
    Args:
        file_path (str): Path to the input text file.
    
    Returns:
        dict: A dictionary containing:
            - dimensions (tuple): (rows, cols) of the grid.
            - num_robots (int): The number of robots.
            - robot_positions (list): List of (x, y) tuples for robot starting positions.
            - rendezvous_point (tuple): (x, y) coordinates of the rendezvous point.
            - grid (list of lists): 2D list representing the grid (0 = free, 1 = obstacle).
    """
    with open(file_path, "r") as file:
        lines = []
        for line in file:
            # Remove inline comments and strip whitespace.
            line = line.split("//")[0].strip()
            if line:
                lines.append(line)
    
    if len(lines) < 4:
        raise ValueError("Input file does not contain enough lines.")
    
    # Parse grid dimensions.
    dims = lines[0].split()
    if len(dims) < 2:
        raise ValueError("First line must contain grid dimensions (rows and cols).")
    rows, cols = int(dims[0]), int(dims[1])
    dimensions = (rows, cols)
    
    # Parse the number of robots.
    num_robots = int(lines[1])
    robot_positions = []
    for i in range(num_robots):
        pos_line = lines[2 + i].split()
        if len(pos_line) < 2:
            raise ValueError("Each robot position must have two integers.")
        robot_positions.append((int(pos_line[0]), int(pos_line[1])))
    
    # Parse the rendezvous point.
    rendezvous_line = lines[2 + num_robots].split()
    if len(rendezvous_line) < 2:
        raise ValueError("Rendezvous point line must contain two integers.")
    rendezvous_point = (int(rendezvous_line[0]), int(rendezvous_line[1]))
    
    # Parse the grid lines.
    grid_lines = lines[3 + num_robots:]
    if len(grid_lines) != rows:
        raise ValueError("Number of grid rows does not match the specified dimensions.")
    
    grid = []
    # The first grid line is assumed to be the top row.
    for line in grid_lines:
        # Convert each character in the line to an integer.
        grid_row = [int(char) for char in line]
        grid.append(grid_row)
    
    return {
        "dimensions": dimensions,
        "num_robots": num_robots,
        "robot_positions": robot_positions,
        "rendezvous_point": rendezvous_point,
        "grid": grid
    }