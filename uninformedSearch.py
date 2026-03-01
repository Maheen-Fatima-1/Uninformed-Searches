import tkinter as tk
import random
import heapq
import math
import time
sizeCell = 30
probSpawning = 0.10
class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding (GBFS and A*)")
        self.rows = 10
        self.cols = 10
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)
        self.grid = []
        self.path = []
        self.agent = self.start
        self.running = False
        self.algorithm = tk.StringVar(value="A*")
        self.heuristic_type = tk.StringVar(value="Manhattan")
        self.dynamic_mode = tk.BooleanVar()
        self.uiGenerateFunction()
        self.makeGrid()
    #MAKING UI
    def uiGenerateFunction(self):
        top = tk.Frame(self.root)
        top.pack(pady=5)
        tk.Label(top, text="Rows:").grid(row=0, column=0)
        self.row_entry = tk.Entry(top, width=5)
        self.row_entry.insert(0, "10")
        self.row_entry.grid(row=0, column=1)
        tk.Label(top, text="Cols:").grid(row=0, column=2)
        self.col_entry = tk.Entry(top, width=5)
        self.col_entry.insert(0, "10")
        self.col_entry.grid(row=0, column=3)
        tk.Button(top, text="Create Grid",
                  command=self.resizeGridFunction).grid(row=0, column=4)
        tk.Label(top, text="Obstacle %:").grid(row=0, column=5)
        self.density_entry = tk.Entry(top, width=5)
        self.density_entry.insert(0, "30")
        self.density_entry.grid(row=0, column=6)
        tk.Button(top, text="Random Map",
                  command=self.makeRandomGrid).grid(row=0, column=7)
        tk.Label(top, text="Algorithm:").grid(row=0, column=8)
        tk.OptionMenu(top, self.algorithm, "GBFS", "A*").grid(row=0, column=9)
        tk.Label(top, text="Heuristic:").grid(row=0, column=10)
        tk.OptionMenu(top, self.heuristic_type,
                      "Manhattan", "Euclidean").grid(row=0, column=11)
        tk.Checkbutton(top, text="Dynamic Mode",
                       variable=self.dynamic_mode).grid(row=0, column=12)
        tk.Button(top, text="Start Search",
                  command=self.startSearching).grid(row=0, column=13)
    #DASHBOARD
        self.dashboard = tk.Frame(self.root)
        self.dashboard.pack(pady=5)
        self.nodes_visited_label = tk.Label(self.dashboard, text="Nodes Visited: 0")
        self.nodes_visited_label.grid(row=0, column=0, padx=5)
        self.path_cost_label = tk.Label(self.dashboard, text="Path Cost: 0")
        self.path_cost_label.grid(row=0, column=1, padx=5)
        self.exec_time_label = tk.Label(self.dashboard, text="Execution Time: 0 ms")
        self.exec_time_label.grid(row=0, column=2, padx=5)
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.wallToggle)
    #MAKE GRID
    def makeGrid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.canvas.config(width=self.cols * sizeCell,
                           height=self.rows * sizeCell)
        self.drawGrid()
    def drawGrid(self, frontier=set(), visited=set()):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                color = "white"
                cell = (r, c)
                if self.grid[r][c] == 1:
                    color = "black"
                elif cell in visited:
                    color = "red"
                elif cell in frontier:
                    color = "yellow"
                if cell == self.start:
                    color = "orange"
                elif cell == self.goal:
                    color = "purple"
                elif cell == self.agent:
                    color = "cyan"
                elif cell in self.path:
                    color = "green"
                self.canvas.create_rectangle(
                    c * sizeCell, r * sizeCell,
                    (c + 1) * sizeCell, (r + 1) * sizeCell,
                    fill=color, outline="gray"
                )
    def resizeGridFunction(self):
        self.rows = int(self.row_entry.get())
        self.cols = int(self.col_entry.get())
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)
        self.agent = self.start
        self.makeGrid()
    def makeRandomGrid(self):
        density = float(self.density_entry.get()) / 100
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = 1 if random.random() < density else 0
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.goal[0]][self.goal[1]] = 0
        self.drawGrid()
    def wallToggle(self, event):
        r = event.y // sizeCell
        c = event.x // sizeCell
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] ^= 1
                self.drawGrid()
    def heuristic(self, a, b):
        if self.heuristic_type.get() == "Manhattan":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    def startSearching(self):
        self.agent = self.start
        self.running = True
        self.planingPath()
        if self.path and self.path[0] == self.agent:
            self.path.pop(0)
        self.stepBystep()
    def planingPath(self):
        if self.algorithm.get() == "GBFS":
            self.path = self.gbfs(self.agent)
        else:
            self.path = self.astar(self.agent)
    #GBFS
    def gbfs(self, start):
        start_time = time.time()
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        visited = set()
        nodes_visited = 0
        while open_list:
            frontier = set([item[1] for item in open_list])
            self.drawGrid(frontier, visited)
            self.root.update()
            _, current = heapq.heappop(open_list)
            nodes_visited += 1
            if current == self.goal:
                break
            visited.add(current)
            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = current[0]+dr, current[1]+dc
                nxt = (nr, nc)
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == 1 or nxt in visited:
                        continue
                    h = self.heuristic(nxt, self.goal)
                    heapq.heappush(open_list, (h, nxt))
                    came_from[nxt] = current
        exec_time = int((time.time() - start_time) * 1000)
        self.nodes_visited_label.config(text=f"Nodes Visited: {nodes_visited}")
        path_cost = len(self.BuildPathAgain(came_from, start)) - 1
        self.path_cost_label.config(text=f"Path Cost: {path_cost}")
        self.exec_time_label.config(text=f"Execution Time: {exec_time} ms")
        return self.BuildPathAgain(came_from, start)
    #A*
    def astar(self, start):
        start_time = time.time()
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_cost = {start: 0}
        visited = set()
        nodes_visited = 0
        while open_list:
            frontier = set([item[1] for item in open_list])
            self.drawGrid(frontier, visited)
            self.root.update()
            _, current = heapq.heappop(open_list)
            nodes_visited += 1
            visited.add(current)
            if current == self.goal:
                break
            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = current[0]+dr, current[1]+dc
                nxt = (nr, nc)
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == 1:
                        continue
                    new_g = g_cost[current] + 1
                    if nxt not in g_cost or new_g < g_cost[nxt]:
                        g_cost[nxt] = new_g
                        f = new_g + self.heuristic(nxt, self.goal)
                        heapq.heappush(open_list, (f, nxt))
                        came_from[nxt] = current
        exec_time = int((time.time() - start_time) * 1000)
        self.nodes_visited_label.config(text=f"Nodes Visited: {nodes_visited}")
        path_cost = len(self.BuildPathAgain(came_from, start)) - 1
        self.path_cost_label.config(text=f"Path Cost: {path_cost}")
        self.exec_time_label.config(text=f"Execution Time: {exec_time} ms")
        return self.BuildPathAgain(came_from, start)

    #REBUILD PATH
    def BuildPathAgain(self, came_from, start):
        path = []
        current = self.goal
        while current in came_from:
            path.append(current)
            current = came_from[current]
        if path:
            path.append(start)
            path.reverse()
        return path

    #DYNAMIC OBSTACLES
    def wallSpawn(self):
        if random.random() > probSpawning:
            return None
        r = random.randint(0, self.rows - 1)
        c = random.randint(0, self.cols - 1)
        cell = (r, c)
        if cell not in [self.start, self.goal, self.agent]:
            if self.grid[r][c] == 0:
                self.grid[r][c] = 1
                return cell
        return None
    
    def stepBystep(self):
        if not self.running:
            return
        if not self.path:
            self.running = False
            return
        next_cell = self.path.pop(0)
        if self.grid[next_cell[0]][next_cell[1]] == 1:
            self.planingPath()
            if self.path and self.path[0] == self.agent:
                self.path.pop(0)
            self.root.after(300, self.stepBystep)
            return
        self.agent = next_cell
        self.drawGrid()
        if self.dynamic_mode.get():
            spawned = self.wallSpawn()
            if spawned and spawned in self.path:
                self.planingPath()
                if self.path and self.path[0] == self.agent:
                    self.path.pop(0)
        if self.agent == self.goal:
            self.running = False
            return
        self.root.after(300, self.stepBystep)
if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()