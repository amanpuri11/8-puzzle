# 8-Puzzle Solver

An interactive, web-based visualization tool that computes and displays the optimal sequence of moves to solve any solvable 8-puzzle configuration. Built with **Streamlit**, this dashboard allows users to define custom initial states, track algorithmic efficiency metrics, and walk through step-by-step solutions visually.

## 🚀 Key Features

* **Interactive Matrix Input:** Seamlessly configure the starting state of the $3 \times 3$ grid using drop-down selectors for each coordinate (Row 1-3, Column 1-3) with instant duplicate checking.
* **Performance Analysis:** Real-time feedback on the efficiency of the search algorithm, highlighting:
  * **States Explored:** The number of unique configurations analyzed during the search.
  * **Total Moves:** The absolute minimum number of steps required to transition to the goal state.
* **Step-by-Step Visualization:** Clear, terminal-style rendering of the board's state after each consecutive slide-move, letting you trace the exact path from start to finish.

## 🛠️ Tech Stack

* **Frontend Dashboard:** Streamlit
* **Algorithm Backend:** Python 3 (Graph-search / Heuristic Pathfinding)
* **Data Structures:** NumPy (Efficient matrix operations and grid state tracking)

## 🧠 How It Works

1. **Input Grid:** Select the tile placement for your custom layout. The "Empty" option represents the blank tile.
2. **Pathfinding:** Once you click **Solve Now**, the backend runs a search algorithm (such as $A^*$ with Manhattan distance or Breadth-First Search) to compute the state transitions.
3. **Execution Analysis:** View the total node expansions ("States Explored") to see how much computational work was done to reach the solution.
4. **Step-by-Step Walkthrough:** Scroll through the sequential grid displays under the "Step-by-Step Visualization" section to physically reproduce the sliding maneuvers.
