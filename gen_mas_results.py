import numpy as np
import heapq
import random

random.seed(42)
np.random.seed(42)

NORMAL, BLOCKED, HOTSPOT, HOME = 0, 1, 2, 3

class GridWorld:
    def __init__(self, blocked_cells=None):
        self.rows, self.cols = 10, 10
        self.grid = np.zeros((10, 10), dtype=int)
        self.hotspot_cells = [(0, 1), (0, 6), (2, 0), (9, 2), (4, 3), (6, 5)]
        for r, c in self.hotspot_cells: self.grid[r][c] = HOTSPOT
        self.home_cells = [(3, 9), (6, 2), (7, 4), (9, 8), (1, 8), (5, 0)]
        for r, c in self.home_cells: self.grid[r][c] = HOME
        self.blocked_cells = blocked_cells if blocked_cells else [(0,3), (1,2), (2,4), (3,1), (4,5), (5,7), (7,1), (8,3)]
        for r, c in self.blocked_cells: self.grid[r][c] = BLOCKED
    def get_neighbours(self, r, c):
        res = []
        for dr, dc in [(-1,0),(1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<10 and 0<=nc<10 and self.grid[nr][nc] != BLOCKED: res.append((nr,nc))
        return res

class Passenger:
    def __init__(self, loc, dest):
        self.location, self.destination = loc, dest
        self.is_drunk = random.random() < 0.3

class TaxiAgent:
    def __init__(self, id, pos):
        self.id, self.position = id, pos
        self.score, self.steps, self.available = 0, 0, True
    def move(self, n):
        self.position = n
        self.steps += 1
        self.score -= 1
    def pickup(self, p):
        self.available = False
        if p.is_drunk: self.score -= 2; self.steps += 2
        return 5 if p.location in [(0,1),(0,6),(2,0),(9,2),(4,3),(6,5)] else 0
    def dropoff(self):
        self.score += 20
        self.available = True

def astar(w, s, g):
    h = lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1])
    q = [(h(s,g), 0, s, [s])]
    v = {}
    while q:
        f, cost, curr, path = heapq.heappop(q)
        if curr == g: return path
        if curr in v and v[curr] <= cost: continue
        v[curr] = cost
        for n in w.get_neighbours(*curr):
            heapq.heappush(q, (cost+1+h(n,g), cost+1, n, path+[n]))
    return None

def run_mas():
    w = GridWorld()
    agents = [TaxiAgent(1, (0,0)), TaxiAgent(2, (9,9))]
    passengers = [Passenger((0,1),(3,9)), Passenger((9,2),(7,4)), Passenger((2,0),(6,2)), Passenger((6,5),(5,0))]
    active = []
    
    while passengers or active:
        for p in passengers[:]:
            av = [a for a in agents if a.available]
            if av:
                a = min(av, key=lambda x: abs(x.position[0]-p.location[0]) + abs(x.position[1]-p.location[1]))
                a.available = False
                path = astar(w, a.position, p.location)
                active.append({'a':a, 'p':p, 'path':path[1:], 'phase':'pickup'})
                passengers.remove(p)
        for t in active[:]:
            if t['path']: t['a'].move(t['path'].pop(0))
            else:
                if t['phase'] == 'pickup':
                    t['a'].pickup(t['p'])
                    t['path'] = astar(w, t['a'].position, t['p'].destination)[1:]
                    t['phase'] = 'dropoff'
                else:
                    t['a'].dropoff()
                    active.remove(t)
    return agents

agents = run_mas()
print(f"Agent 1 Score: {agents[0].score}, Steps: {agents[0].steps}")
print(f"Agent 2 Score: {agents[1].score}, Steps: {agents[1].steps}")
print(f"Total Fleet Score: {agents[0].score + agents[1].score}")
print(f"Parallel Steps: {max(agents[0].steps, agents[1].steps)}")
