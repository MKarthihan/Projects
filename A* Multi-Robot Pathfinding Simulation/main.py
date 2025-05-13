import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from environment import Environment
from robot import Robot
import metrics
import matplotlib.colors as mcolors
import communication
from metrics import log_metrics
import datetime

run_started = False

def display_environment(env, robots, ax):
    """
    Renders the environment on the given Axes, marking obstacles, robot positions, and the rendezvous point.
    Uses a custom color map and draws grid lines.
    
    Args:
        env (Environment): The simulation environment.
        robots (list): List of Robot instances.
        ax (matplotlib.axes.Axes): The axes to draw the grid.
    """
    #clear previous frame
    ax.clear()

    grid = np.array(env.grid)
    grid_disp = grid.copy()

    # Mark each robot position with value 2 (blue).
    for robot in robots:
        x, y = robot.position
        grid_disp[y][x] = 2

    rx, ry = env.rendezvous_point
    grid_disp[ry][rx] = 3

    # Define a custom color map for values 0, 1, 2, 3:
    # 0 => white / free space, 1 => black / obstical, 2 => blue / robot, 3 => red / rendezvous point
    cmap = mcolors.ListedColormap(["white", "black", "blue", "red"])
    #boundaries to separate each discrete color
    norm = mcolors.BoundaryNorm([0, 1, 2, 3, 4], cmap.N)

    ax.imshow(grid_disp, cmap=cmap, norm=norm)

    rows, cols = env.dimensions  # (rows, columns)

    #ticks at every integer
    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))

    #label the ticks (0..cols-1) and (0..rows-1) for both axes
    ax.set_xticklabels(np.arange(cols))
    ax.set_yticklabels(np.arange(rows))

    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)

    #grid lines
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
    #hide major tick grid lines
    ax.grid(which='major', visible=False)

    # Make minor tick lines invisible
    ax.tick_params(which='minor', length=0)

    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title("Robot Simulation\nBlue Robots, Red Rendezvous")

    #updated plot rendered
    plt.draw()

def run_simulation(env, robots, ax, max_iterations=50, pause_time=0.5, wait_threshold=2):
    steps = 0
    simulation_start = time.time()
    waiting_counters = {robot.id: 0 for robot in robots}

    while steps < max_iterations and not all(robot.finished for robot in robots):
        reserved_cells = set()

        #process robots in order of priority (lowest id first)
        for robot in sorted(robots, key=lambda r: r.id):
            if robot.finished:
                continue

            robot.communicate()
            robot.receive_communications()

            if not robot.path:
                robot.plan_path()

            #determine intended move (using robot.path[1] if available).
            intended = robot.path[1] if len(robot.path) >= 2 else None
            if intended is None:
                continue

            if intended == env.rendezvous_point:
                robot.move()
                reserved_cells.add(robot.position)
                waiting_counters[robot.id] = 0
                continue

            if intended in reserved_cells:
                waiting_counters[robot.id] += 1
                print(f"Robot {robot.id} waiting due to conflict at {intended} (wait count: {waiting_counters[robot.id]})")
                # If waiting too long, force a re-plan.
                if waiting_counters[robot.id] >= wait_threshold:
                    print(f"Robot {robot.id} forcing re-plan after waiting at {intended}")
                    robot.plan_path()
                    waiting_counters[robot.id] = 0
                continue
            else:
                waiting_counters[robot.id] = 0
            robot.move()
            reserved_cells.add(robot.position)

        communication.global_messages.clear()
        display_environment(env, robots, ax)
        plt.pause(pause_time)
        steps += 1

    simulation_end = time.time()
    exec_time = metrics.compute_execution_time(simulation_start, simulation_end)
    #need to fix show algorithm completion time not animation time
    print(f"Simulation completed in {steps} steps and {exec_time:.2f} seconds.")

    display_environment(env, robots, ax)
    ax.text(0.5, 0.95, f"Algorithm Execution Time: {exec_time:.2f} sec",
            transform=ax.transAxes, fontsize=12, color='black', ha='center', va='top',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

    for robot in robots:
        path = robot.full_path
        if not path or len(path) < 2:
            continue

        xs = [pos[0] for pos in path]
        ys = [pos[1] for pos in path]
        ax.plot(xs, ys, linestyle="--", marker="o", label=f"Robot {robot.id} Path")

    ax.legend()
    plt.draw()
    plt.pause(8)
    plt.close('all')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_metrics({"Simulation Run": timestamp}, log_file="metrics.log")

    summary_data = {
        "Total Simulation Steps": steps,
        "Total Execution Time (sec)": round(exec_time, 2)
    }
    log_metrics(summary_data, log_file="metrics.log")

    for robot in robots:
        robot_data = {
            f"Robot {robot.id} Stats": "",
            "Steps Taken": robot.steps_taken,
            "Replans": robot.replans,
        }
        log_metrics(robot_data, log_file="metrics.log")

    return exec_time, steps

def main():
    input_file = "input3.txt"
    env = Environment.read_from_file(input_file)

    robots = [Robot(i, pos, env) for i, pos in enumerate(env.robot_positions, start=1)]

    print("Environment Loaded:")
    print("Dimensions:", env.dimensions)
    print("Rendezvous Point:", env.rendezvous_point)
    print("Robot Starting Positions:", env.robot_positions)
    print("Obstacles:", env.obstacles)

    #figure and axes
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    display_environment(env, robots, ax)

    def on_play(event):
        global run_started
        if run_started:
            return
        run_started = True
        play_button.ax.set_visible(False)
        plt.draw()
        run_simulation(env, robots, ax)

    button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
    play_button = Button(button_ax, 'Play')
    play_button.on_clicked(on_play)

    plt.show()

if __name__ == "__main__":
    main()