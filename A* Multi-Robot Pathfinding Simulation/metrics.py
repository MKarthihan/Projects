import time

def compute_execution_time(start_time, end_time):
    """
    Computes the execution time between two timestamps.
    
    Args:
        start_time (float): The start time (e.g., from time.time()).
        end_time (float): The end time.
        
    Returns:
        float: The elapsed time in seconds.
    """
    return end_time - start_time

def evaluate_path_optimality(path):
    """
    Evaluates the optimality of a given path.
    
    For this example, we define the path optimality based on the number of steps in the path.
    A shorter path (fewer steps) is considered more optimal. In a more advanced setting, this
    could compare the computed path against a known shortest path.
    
    Args:
        path (list): A list of (x, y) tuples representing the path.
        
    Returns:
        int: The number of steps in the path (lower is more optimal).
             Returns infinity if no path is found.
    """
    if path is None:
        return float('inf')
    #subtract 1 because the starting position is included in the path.
    return len(path) - 1

def log_metrics(metrics_data, log_file="metrics.log"):
    """
    Logs performance metrics to a specified log file.
    
    Args:
        metrics_data (dict): A dictionary where keys are metric names and values are their measurements.
        log_file (str): The file path to which the metrics should be appended.
    """
    with open(log_file, "a") as f:
        f.write("Metrics Log Entry:\n")
        for key, value in metrics_data.items():
            f.write(f"{key}: {value}\n")
        f.write("-" * 40 + "\n")