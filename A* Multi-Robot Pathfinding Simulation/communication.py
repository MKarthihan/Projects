# Global list to store broadcast messages.
# Each message is a tuple: (robot_id, obstacles), where obstacles is a list of (x, y) tuples
global_messages = []

def broadcast_obstacle_data(robot_id, obstacles):
    """
    Broadcasts obstacle data from a robot to all other robots.
    
    Args:
        robot_id (int): The ID of the broadcasting robot.
        obstacles (list): A list of (x, y) tuples representing the detected obstacles.
    """
    global global_messages
    global_messages.append((robot_id, obstacles))
    print(f"Robot {robot_id} broadcasted obstacles: {obstacles}")

def receive_obstacle_data(robot_id):
    """
    Retrieves obstacle data broadcast by other robots.
    
    Args:
        robot_id (int): The ID of the robot receiving data.
        
    Returns:
        list: A list of (x, y) tuples representing obstacles broadcast by other robots.
    """
    received = []
    for sender_id, obstacles in global_messages:
        if sender_id != robot_id:
            received.extend(obstacles)
    return received