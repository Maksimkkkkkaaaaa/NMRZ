import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
sys.path.insert(0, PROJECT_ROOT)

from src.tsp import generate_random_cities, compute_distance_matrix
from src.ga import run_ga
from src.utils import print_tour


def main():
    cities = generate_random_cities()
    dist_matrix = compute_distance_matrix(cities)

    print(f"Сгенерировано {len(cities)} городов.")
    best_tour, best_len = run_ga(cities, dist_matrix)

    print("\n=== Результат ===")
    print_tour(best_tour, cities, dist_matrix)
    print(f"Итоговая длина: {best_len:.3f}")


if __name__ == "__main__":
    main()
