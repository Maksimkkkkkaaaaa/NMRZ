import math
import random
from src.config import NUM_CITIES, X_MIN, X_MAX, Y_MIN, Y_MAX, RANDOM_SEED

class City:
    def __init__(self, index: int, x: float, y: float):
        self.index = index
        self.x = x
        self.y = y

    def __repr__(self):
        return f"City({self.index}, x={self.x:.1f}, y={self.y:.1f})"

def generate_random_cities(num_cities=NUM_CITIES):
    random.seed(RANDOM_SEED)
    cities = []
    for i in range(num_cities):
        x = random.uniform(X_MIN, X_MAX)
        y = random.uniform(Y_MIN, Y_MAX)
        cities.append(City(i, x, y))
    return cities

def compute_distance_matrix(cities):
    n = len(cities)
    dist_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dx = cities[i].x - cities[j].x
            dy = cities[i].y - cities[j].y
            d = math.hypot(dx, dy)
            dist_matrix[i][j] = d
            dist_matrix[j][i] = d
    return dist_matrix
