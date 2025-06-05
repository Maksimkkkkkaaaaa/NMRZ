import random
from copy import deepcopy

from src.config import (
    POPULATION_SIZE,
    NUM_GENERATIONS,
    CROSSOVER_PROB,
    MUTATION_PROB,
    TOURNAMENT_SIZE,
    ELITISM_COUNT,
    EPSILON,
)
from src.utils import tour_length


def create_initial_population(num_cities, pop_size=POPULATION_SIZE):
    population = []
    base = list(range(num_cities))
    for _ in range(pop_size):
        indiv = base[:]
        random.shuffle(indiv)
        population.append(indiv)
    return population


def fitness_of(indiv, dist_matrix):
    length = tour_length(indiv, dist_matrix)
    return 1.0 / (length + EPSILON)


def tournament_selection(population, fitnesses, k=TOURNAMENT_SIZE):
    chosen = random.sample(range(len(population)), k)
    best = chosen[0]
    for idx in chosen[1:]:
        if fitnesses[idx] > fitnesses[best]:
            best = idx
    return deepcopy(population[best])


def order_crossover(parent1, parent2):
    size = len(parent1)
    child1 = [-1] * size
    child2 = [-1] * size

    i, j = sorted(random.sample(range(size), 2))

    for idx in range(i, j):
        child1[idx] = parent1[idx]
        child2[idx] = parent2[idx]

    missing1 = [gene for gene in parent2 if gene not in child1]
    fill_positions1 = [idx for idx, val in enumerate(child1) if val == -1]
    for k, pos in enumerate(fill_positions1):
        child1[pos] = missing1[k]

    missing2 = [gene for gene in parent1 if gene not in child2]
    fill_positions2 = [idx for idx, val in enumerate(child2) if val == -1]
    for k, pos in enumerate(fill_positions2):
        child2[pos] = missing2[k]

    return child1, child2


def swap_mutation(indiv):
    a, b = random.sample(range(len(indiv)), 2)
    indiv[a], indiv[b] = indiv[b], indiv[a]


def evolve_population(population, dist_matrix):
    pop_size = len(population)
    fitnesses = [fitness_of(ind, dist_matrix) for ind in population]

    sorted_indices = sorted(range(pop_size), key=lambda i: fitnesses[i], reverse=True)
    new_population = []

    for idx in sorted_indices[:ELITISM_COUNT]:
        new_population.append(deepcopy(population[idx]))

    while len(new_population) < pop_size:
        parent1 = tournament_selection(population, fitnesses)
        parent2 = tournament_selection(population, fitnesses)

        if random.random() < CROSSOVER_PROB:
            child1, child2 = order_crossover(parent1, parent2)
        else:
            child1, child2 = parent1[:], parent2[:]

        if random.random() < MUTATION_PROB:
            swap_mutation(child1)
        if random.random() < MUTATION_PROB:
            swap_mutation(child2)

        new_population.append(child1)
        if len(new_population) < pop_size:
            new_population.append(child2)

    fitnesses_new = [fitness_of(ind, dist_matrix) for ind in new_population]
    return new_population, fitnesses_new


def run_ga(cities, dist_matrix):
    num_cities = len(cities)
    population = create_initial_population(num_cities)

    best_overall = None
    best_fitness = -1.0

    for gen in range(NUM_GENERATIONS):
        population, fitnesses = evolve_population(population, dist_matrix)

        gen_best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
        gen_best_fit = fitnesses[gen_best_idx]

        if gen_best_fit > best_fitness:
            best_fitness = gen_best_fit
            best_overall = population[gen_best_idx][:]

        if gen % 50 == 0 or gen == NUM_GENERATIONS - 1:
            best_length_so_far = 1.0 / (best_fitness + EPSILON)
            print(f"Поколение {gen:4d} | Лучший путь длиной ≈ {best_length_so_far:.3f}")

    best_length = tour_length(best_overall, dist_matrix)
    return best_overall, best_length
