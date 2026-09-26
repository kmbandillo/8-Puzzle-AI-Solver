# 8-Puzzle Solver with Pygame GUI

#### An interactive 8-Puzzle game and AI solver developed in Python. The application allows users to manually solve the puzzle or utilize search algorithms **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, and **A\* Search**.  It displays the path cost, explored states, and step-by-step solution moves.
---

## Features

- **Interactive Game Board**: Click adjacent tiles to manually slide them into the blank space (`0`).
- **Solvability Verification**: Automatically determines whether the input configuration is mathematically solvable using inversion counting.
- **Multiple AI Search Algorithms**:
  - **BFS (Breadth-First Search)**: Guarantees the shortest path cost / optimal sequence of moves.
  - **DFS (Depth-First Search)**: Explores deep branches first (with a depth limit of 200).
  - **A\* Search**: Uses the Manhattan Distance heuristic combined with path cost ($f(n) = g(n) + h(n)$) to efficiently find the optimal solution.
- **On-Screen Results Display**:
  - Shows **Path cost**, **Explored states**, and the move sequence (**SOLUTION: ...**).
- **Step-by-Step Move Player ("Next" Button)**: Step through the generated solution one move at a time with animated tile transitions.
- **Victory Screen**: Automatically detects the goal state and presents a win screen with an Exit button.

---

## Configuration & Files

### Input File: `puzzle.in`
The initial state of the 8-puzzle board is loaded from the **`puzzle.in`** configuration file located in the root directory.

#### Format:
- The file contains exactly **3 lines**, with each line containing **3 space-separated integers** from `0` to `8`.
- The number **`0`** represents the **blank (empty) space**.

#### Example `puzzle.in`:
```text
2 3 0
1 5 6
4 7 8
```
In this example:
- Row 1: `2`, `3`, and the blank tile `0`
- Row 2: `1`, `5`, `6`
- Row 3: `4`, `7`, `8`

### Output File: `puzzle.out`
When the **Solution** button is pressed, the resulting sequence of actions is saved to **`puzzle.out`**.

- Move notations:
  - `U`: Move blank space **Up**
  - `D`: Move blank space **Down**
  - `L`: Move blank space **Left**
  - `R`: Move blank space **Right**

#### Example `puzzle.out`:
```text
L L D D R R 
```
---

## Requirements & Installation

1. **Python 3.8+**
2. **Pygame** library

To install Pygame, run:
```bash
pip install pygame
```

---

## How to Run

1. Configure your starting puzzle state in `puzzle.in`.
2. Run the main script:
   ```bash
   python game.py
   ```
3. **Gameplay Controls**:
   - **Manual Play**: Click any tile adjacent to the blank space to slide it.
   - **Select Algorithm**: Click the **CHOOSE** dropdown and select **BFS**, **DFS**, or **A\***.
   - **Find Solution**: Click **Solution**. The statistics (`Path cost:`, `Explored states:`, `SOLUTION:`) will appear in the scrollable box below the buttons, and moves will be saved to `puzzle.out`.
   - **Scroll Results**: Use your **mouse wheel** (up/down) or **click-and-drag** inside the solution box if the solution text exceeds the box height.
   - **Animate Moves**: Click **Next** to step through the solution tile by tile until the goal state is achieved.
   - **Exit**: Click **Exit** or close the window.
