GRID_ROWS = 100
GRID_COLS = 200

SHELVES = [
    *[(0, c) for c in range(GRID_COLS)],
    *[(GRID_ROWS-1, c) for c in range(GRID_COLS)],
    *[(r, 0) for r in range(GRID_ROWS)],
    *[(r, GRID_COLS-1) for r in range(GRID_ROWS)],
    (3,3), (3,4), (3,5),
    (6,7), (6,8), (6,9)
]

ORDERS = [
    (1,2), (2,8), (4,6), (5,10),
    (7,3), (8,5), (2,4), (6,2)
]

PACK_ZONE = (1, GRID_COLS-2)

DOCK_STATIONS = [
    (1,1),
    (1, GRID_COLS-3),
    (GRID_ROWS-2,1),
    (GRID_ROWS-2, GRID_COLS-3)
]

NUM_AGENTS = len(DOCK_STATIONS)

MAX_STEPS = 200

