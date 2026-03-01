# Uninformed-Searches
Python project implementing GBFS and A* pathfinding on a dynamic grid
# Dynamic Pathfinding (GBFS & A*)
This project implements **Greedy Best-First Search (GBFS)** and **A* Search** on a dynamic 2D grid using Python and Tkinter. The grid allows the user to place obstacles, resize, and spawn dynamic obstacles while the agent moves. The program visually shows the pathfinding process and relevant statistics.

---

## **Features**

- Grid resizing (custom rows and columns)
- Random obstacle generation
- Start and goal placement
- **GBFS** and **A\*** pathfinding algorithms
- Manhattan and Euclidean heuristics
- Dynamic mode: obstacles spawn while the agent moves
- Visualization of:
  - Agent position
  - Frontier and visited nodes
  - Path found
- Dashboard showing:
  - Nodes visited
  - Path cost
  - Execution time (in ms)

---

## **Requirements**

- Python 3.x
- Tkinter (usually included with Python)

---

## **How to Run**

1. Clone the repository:

```bash
git clone https://github.com/Maheen-Fatima-1/Uninformed-Searches.git
```
2. Navigate to the project folder:
```bash
cd Uninformed-Searches
```
3. Run the program:
```bash
python uninformedSearch.py
```
## Usage

1. Enter the number of rows and columns for the grid.
2. Generate a random map or manually click cells to toggle obstacles.
3. Select the algorithm (**GBFS** or **A***).
4. Select the heuristic (**Manhattan** or **Euclidean**).
5. Enable **Dynamic Mode** if you want obstacles to spawn while the agent moves.
6. Click **Start Search** to visualize the agent moving toward the goal.

Enable Dynamic Mode if you want obstacles to spawn while the agent moves.

Click Start Search to visualize the agent moving toward the goal.
