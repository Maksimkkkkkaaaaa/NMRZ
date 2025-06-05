from src.tsp import compute_distance_matrix, generate_random_cities

def tour_length(tour, dist_matrix):
    total = 0.0
    n = len(tour)
    for k in range(n):
        i = tour[k]
        j = tour[(k + 1) % n]
        total += dist_matrix[i][j]
    return total

def print_tour(tour, cities, dist_matrix):
    print("Лучший маршрут (индексы городов):")
    print(" -> ".join(str(idx) for idx in tour) + f" -> {tour[0]} (возврат)")
    print("\nПоследовательность координат:")
    for idx in tour:
        city = cities[idx]
        print(f"  City {city.index}: ({city.x:.2f}, {city.y:.2f})")
    city0 = cities[tour[0]]
    print(f"  City {city0.index}: ({city0.x:.2f}, {city0.y:.2f})  (возврат)\n")
    length = tour_length(tour, dist_matrix)
    print(f"Суммарная длина маршрута: {length:.3f}")
    return length

def prepare_problem():
    cities = generate_random_cities()
    dist_matrix = compute_distance_matrix(cities)
    return cities, dist_matrix
