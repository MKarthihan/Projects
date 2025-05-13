import heapq
import math

def heuristic(current, goal, method="Manhattan"):
    """
    Calculates the heuristic distance between the current node and the goal node.
    
    Args:
        current (tuple): (x, y) coordinates of the current node.
        goal (tuple): (x, y) coordinates of the goal node.
        method (str): Type of heuristic to use ("Manhattan" or "Euclidean").
        
    Returns:
        float: The heuristic cost estimate.
    """
    (x1, y1) = current
    (x2, y2) = goal
    if method == "Manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    elif method == "Euclidean":
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        raise ValueError("Unsupported heuristic method. Use 'Manhattan' or 'Euclidean'.")

def get_neighbors(current, grid):
    """
    Retrieves the valid neighboring cells (up, down, left, right) for a given node.
    
    Args:
        current (tuple): (x, y) coordinate of the current node.
        grid (list of lists): 2D grid representation where 0 indicates free cell and 1 indicates an obstacle.
        
    Returns:
        list: A list of (x, y) coordinates for valid neighbors.
    """
    neighbors = []
    x, y = current
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        #check if within grid bounds
        if 0 <= nx < cols and 0 <= ny < rows:
            #check if the cell is free (0 means free, 1 means obstacle)
            if grid[ny][nx] == 0:
                neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(came_from, current):
    """
    Reconstructs the path from start to goal using the came_from mapping.
    
    Args:
        came_from (dict): A mapping of nodes to their predecessors.
        current (tuple): The goal node.
        
    Returns:
        list: A list of nodes representing the path from start to goal.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star(start, goal, grid, heuristic_func=heuristic):
    """
    Executes the A* algorithm to find the shortest path from start to goal in a grid.
    
    Args:
        start (tuple): Starting (x, y) coordinate.
        goal (tuple): Goal (x, y) coordinate.
        grid (list of lists): 2D grid representation (0 = free cell, 1 = obstacle).
        heuristic_func (function): Function to calculate heuristic cost. Default is Manhattan distance.
        
    Returns:
        list: The optimal path from start to goal as a list of (x, y) tuples,
              or None if no path is found.
    """
    #initialize open set as a priority queue and add start node
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}  #to reconstruct the path later
    g_cost = {start: 0}  #cost from start to current node
    
    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor in get_neighbors(current, grid):
            dx = abs(neighbor[0] - current[0])
            dy = abs(neighbor[1] - current[1])
            step_cost = 1
            tentative_g_cost = g_cost[current] + step_cost
            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic_func(neighbor, goal)
                heapq.heappush(open_set, (f_cost, neighbor))
                
    #no path found
    return None