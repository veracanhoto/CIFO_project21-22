from charles.charles import Population, Individual
from data.tsp_data import distance_matrix
from copy import deepcopy
from charles.selection import fps, tournament, ranking
from charles.mutation import swap_mutation, inversion_mutation
from charles.crossover import cycle_co, pmx_co
import numpy as np
import time
import pandas as pd
import numpy as np
import plotly.express as px


def get_fitness(self):
    """A simple objective function to calculate distances
    for the TSP problem.

    Returns:
        int: the total distance of the path
    """
    fitness = 0
    for i in range(len(self.representation)):
        fitness += distance_matrix[self.representation[i - 1]][self.representation[i]]
    return int(fitness)




def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switches
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation) - 1)]

    for count, i in enumerate(n):
        i[count], i[count + 1] = i[count + 1], i[count]

    n = [Individual(i) for i in n]
    return n


# Monkey patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours



# From the charles lib

selection_applied = [fps, tournament,ranking]
crossover_applied = [cycle_co, pmx_co]
mutation_applied = [swap_mutation, inversion_mutation]

names = ["fps_cycle_swap", "fps_cycle_inversion", "fps_pmx_swap", "fps_pmx_inversion",
         "tournament_cycle_swap", "tournament_cycle_inversion", "tournament_pmx_swap",
         "tournament_pmx_inversion","ranking_cycle_swap", "ranking_cycle_inversion",
         "ranking_pmx_swap", "ranking_pmx_inversion",
         ]

fitness_per_combination = []
final_df = pd.DataFrame()

count = 0
for selection in selection_applied:
    for crossover in crossover_applied:
        for mutation in mutation_applied:
            average_final_fit = 0
            fitness_progression_average = []
            time_average = 0
            for j in range(100):
                start = time.time()
                pop = Population(
                    size=25,
                    sol_size=len(distance_matrix[0]),
                    valid_set=[j for j in range(len(distance_matrix[0]))],
                    replacement=False,
                    optim="min",
                )

                pop.evolve(
                    gens=100,
                    select=selection,
                    crossover=crossover,
                    mutate=mutation,
                    co_p=0.8,
                    mu_p=0.1,
                    elitism=True
                )

                end = time.time()
                time_average += (end-start)

                average_final_fit += pop.fit_display[-1]
                fitness_progression_average.append(pop.fit_display)


            average_final_fit = average_final_fit / 100
            fitness_per_combination.append(average_final_fit)

            numpy_array = np.array(fitness_progression_average)
            invert = numpy_array.T

            df = pd.DataFrame(invert)

            final_df[names[count]] = df.mean(axis=1)

            count += 1

print(fitness_per_combination)


fig = px.line(final_df)
fig.show()