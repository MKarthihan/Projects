# A* Robot Pathfinding Simulation (Python)

---

Overview:
---------
This project simulates a group of autonomous robots navigating a shared 2D grid environment. 
Each robot uses the A* pathfinding algorithm to reach a common rendezvous point while detecting 
and avoiding obstacles. Robots communicate with each other by sharing obstacle information 
to improve path planning in a decentralized manner.

How to Run:
-----------
1. Ensure you are in the project directory.
2. Make sure `input.txt` is correctly formatted and placed in the same folder.
3. Run the simulation using:

       python main.py

4. Click the "Play" button in the GUI to start the simulation.

Features:
---------
- A* algorithm with selectable Manhattan or Euclidean heuristics
- Local map updates for each robot
- Simple obstacle detection and broadcast-based communication
- Real-time grid visualization with Matplotlib
- Metrics logging for steps, replans, execution time, etc.

Requirements:
-------------
- Python 3.7+
- pip (Python package manager)

Dependencies:
-------------
Install required external libraries with:

    pip install numpy matplotlib

All other libraries used are part of Python's standard library:
- time
- math
- os
- datetime
- heapq
- copy

Project Structure:
------------------
    main.py               ← Entry point; handles GUI and simulation loop
    robot.py              ← Defines Robot class and behavior
    a_star.py             ← Contains A* algorithm and helpers
    communication.py      ← Manages robot-to-robot obstacle sharing
    environment.py        ← Loads grid, obstacles, and robot positions from file
    utils.py              ← Distance functions and file parsing
    metrics.py            ← Logging and performance tracking
    input.txt             ← Required input file to configure environment
    metrics.log           ← (Optional) Created during runtime to log metrics

Input File Format:
------------------
The `input.txt` file must follow this format:

    <rows> <cols>
    <number_of_robots>
    <robot1_x> <robot1_y>
    ...
    <rendezvous_x> <rendezvous_y>
    <grid_row_1>
    <grid_row_2>
    ...
    <grid_row_n>

Legend:
- 0 = free cell
- 1 = obstacle
- Rows are ordered top to bottom (row 0 is the top row)

Output:
-------
- A real-time grid showing robot movement
- Logged metrics (steps, time, robot stats) in `metrics.log`

Notes:
------
- Robots share obstacle information but do not coordinate movement directly.
- The simulation stops either when all robots arrive or after a maximum number of steps.
- You can customize the grid and robot positions in `input.txt`.