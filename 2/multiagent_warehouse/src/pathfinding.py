import heapq

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(pos, warehouse):
    r,c = pos
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if warehouse.is_free(nr, nc):
            yield (nr, nc)

def a_star(start, goal, warehouse, occupied=set()):
    open_set = []
    heapq.heappush(open_set, (manhattan(start, goal), 0, start, [start]))
    visited = set([start])

    while open_set:
        est_total, cost, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        for nb in neighbors(current, warehouse):
            if nb in occupied:
                continue
            new_cost = cost + 1
            if nb not in visited:
                visited.add(nb)
                f_score = new_cost + manhattan(nb, goal)
                heapq.heappush(open_set, (f_score, new_cost, nb, path + [nb]))
    return []
