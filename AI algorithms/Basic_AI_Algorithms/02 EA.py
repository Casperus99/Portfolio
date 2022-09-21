import matplotlib.pyplot as plt
import numpy as np
import random as rand
import time


def calculate_specimen_fitness(x):
    """
    # Shubert Function
    sum1 = 0
    sum2 = 0
    for i in range(1, 6):
        sum1 += (i*np.cos(((i+1)*x[0])+i))
        sum2 += (i*np.cos(((i+1)*x[1])+i))
    function = sum1 * sum2
    """
    function = (1-x[0])**2 + 100*(x[1]-x[0]**2)**2  # Rosenbrock function
    return function


def evolutionary_algorythm(chromosome_length, population_size, max_iter, tournament_size, mutation_power, mutation_probability, elite_size, initial_type):
    initial_population = create_initial_population(chromosome_length, population_size, initial_type)
    initial_population_with_fitness = calculate_population_fitness(initial_population)
    best_specimen, best_fitness = find_best_specimen(initial_population_with_fitness)
    current_population_with_fitness = initial_population_with_fitness
    iter = 0
    best_fitness_list = []
    best_fitness_list.append(best_fitness)
    while(iter <= max_iter):
        iter += 1
        new_population = reproduction(current_population_with_fitness, population_size, tournament_size)
        new_population = crossing(new_population, population_size, chromosome_length)
        new_population = mutation(new_population, mutation_power, mutation_probability)
        new_population_with_fitness = calculate_population_fitness(new_population)
        new_best_specimen, new_best_fitness = find_best_specimen(new_population_with_fitness)
        if new_best_fitness < best_fitness:
            best_fitness = new_best_fitness
            best_specimen = new_best_specimen
        best_fitness_list.append(best_fitness)
        current_population_with_fitness = succession(current_population_with_fitness, new_population_with_fitness, elite_size)
    return best_fitness_list


def create_initial_population(chromosome_length, population_size, initial_type):
    population = []
    if initial_type == 0:
        for i in range(population_size):
            specimen = []
            for gene in range(chromosome_length):
                specimen.append(rand.random()*10-5)
            population.append(specimen)
    else:
        specimen = []
        for gene in range(chromosome_length):
                specimen.append(rand.random()*10-5)
        for i in range(population_size):
            population.append(specimen)
    return population


def calculate_population_fitness(population):
    population_with_fitness = []
    for specimen in population:
        fitness = calculate_specimen_fitness(specimen)
        population_with_fitness.append([specimen, fitness])
    return population_with_fitness
    

def find_best_specimen(population_with_fitness):
    best_specimen = population_with_fitness[0][0]
    best_fitness = population_with_fitness[0][1]
    for specimen, fitness in population_with_fitness:
        if fitness < best_fitness:
            best_specimen = specimen
            best_fitness = fitness
    return [best_specimen, best_fitness]


def reproduction(population_with_fitness, population_size, tournament_size):
    new_population = []
    for tournament in range(population_size):
        participants_with_fitness = []
        for participant in range(tournament_size):
            index = rand.randint(0, population_size-1)
            participants_with_fitness.append(population_with_fitness[index])
        winner, winner_fitness = find_best_specimen(participants_with_fitness)
        new_population.append(winner)
    return new_population


def crossing(population, population_size, chromosome_length):
    new_population = []
    for i in range(int(population_size/2)):
        index_1 = rand.randint(0, population_size-1)
        index_2 = rand.randint(0, population_size-1)
        parent_1 = population[index_1]
        parent_2 = population[index_2]
        child_1 = []
        child_2 = []
        for gene in range(chromosome_length):
            child_1.append(0.1*parent_1[gene] + 0.9*parent_2[gene])
            child_2.append(0.1*parent_2[gene] + 0.9*parent_1[gene])
        new_population.extend([child_1, child_2]) 
    return new_population


def mutation(population, mutation_power, mutation_probability):
    new_population = []
    for specimen in population:
        new_specimen = []
        for gene in specimen:
            if rand.random() <= mutation_probability:
                gene += mutation_power*np.random.normal(0,1,1)[0]
            new_specimen.append(gene)
        new_population.append(new_specimen)
    return new_population


def succession(old_population_with_fitness, pretenders_with_fitness, elite_size):
    new_population_with_fitness = []
    for i in range(elite_size):
        old_elite = find_best_specimen(old_population_with_fitness)
        new_population_with_fitness.append(old_elite)
        index = old_population_with_fitness.index(old_elite)
        old_population_with_fitness.pop(index)
    for i in range(elite_size):
        dying_pretender = find_worst_specimen(pretenders_with_fitness)
        index = pretenders_with_fitness.index(dying_pretender)
        pretenders_with_fitness.pop(index)
    new_population_with_fitness.extend(pretenders_with_fitness)
    return new_population_with_fitness


def find_worst_specimen(population_with_fitness):
    worst_specimen = population_with_fitness[0][0]
    worst_fitness = population_with_fitness[0][1]
    for specimen, fitness in population_with_fitness:
        if fitness > worst_fitness:
            worst_specimen = specimen
            worst_fitness = fitness
    return [worst_specimen, worst_fitness]


if __name__ == "__main__":
    """
    time1 = time.time()
    evolutionary_algorythm(2, 10, 1000, 10, 5, 1, 1, 0)
    time2 = time.time()
    evolutionary_algorythm(2, 20, 1000, 10, 5, 1, 1, 0)
    time3 = time.time()
    evolutionary_algorythm(2, 50, 1000, 10, 5, 1, 1, 0)
    time4 = time.time()
    evolutionary_algorythm(2, 100, 1000, 10, 5, 1, 1, 0)
    time5 = time.time()
    evolutionary_algorythm(2, 200, 1000, 10, 5, 1, 1, 0)
    time6 = time.time()
    evolutionary_algorythm(2, 500, 1000, 10, 5, 1, 1, 0)
    time7 = time.time()
    times = [time2-time1, time3-time2, time4-time3, time5-time4, time6-time5, time7-time6]
    names = ['10', '20', '50', '100', '200', '500']
    plt.bar(names, times)
    plt.title('iter = 1000; turniej = 10')
    """
    plt.plot(evolutionary_algorythm(2, 10, 1000, 10, 5, 1, 1, 0), label='test')
    plt.plot(evolutionary_algorythm(2, 10, 1000, 10, 5, 1, 1, 0), label='test')
    plt.xlabel('iterations')
    plt.ylabel('fitness')
    plt.legend()
    plt.title('test')
    plt.show()
