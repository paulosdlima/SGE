import pygad
import numpy as np
from numpy.random import default_rng

class PygadService:
    
    

    def __init__(self, num_genes, indices, leave_days):
        self.num_genes = num_genes
        self.indices = indices
        self.num_generations = 1000 #número de gerações
        self.num_parents_mating = 50

        self.sol_per_pop = 100  # #número de soluções
        #num_genes = 30 #número de dias na solução

        self.init_range_low = 1 #1 # menor valor do intervalo
        self.init_range_high = 4 #len(indices) - 1 #3 # maior valor do intervalo
        self.gene_space = {'low' : 1, 'high': 4 } #gene_space#{'low' : self.init_range_low, 'high' : self.init_range_high}
        self.leave_days = leave_days
        self.parent_selection_type = "sss"
        self.keep_parents = -1 # numero de pais por padrão "-1"

        self.crossover_type = "single_point" # 

        self.mutation_type = "random"
        self.mutation_percent_genes = 10 # 10% do genes sofrerão mutação
        self.fitness_function = self.fitness_func_shifts()

    def fitness_func_shifts(self):
        def functionValidate(solution, solution_idx):
            penalty = 1;
            
            gene_space = self.gene_space
            ar_unique = np.unique(solution) #lista de valores diferentes
            
            for index, value in enumerate(ar_unique):
                for y in range(self.leave_days-1):
                    if ((index+y) < ar_unique.size and value == ar_unique[index+y]):
                        penalty = penalty+0.1
            fitness = (1/penalty) * 100;
            return fitness
        return functionValidate  


    def fitness_func_shifts_old(self):
        def function1(solution, solution_idx):
            leaves = 4
            fitness = 0
            penalty = 0
            ar_unique = np.unique(solution) #lista de valores diferentes
            if (ar_unique.size < self.init_range_high - self.init_range_low):
                penalty = penalty + 10 * ((self.init_range_high - self.init_range_low) - ar_unique.size)   
            for x in ar_unique:
                indices = self.indices#list(np.where(self.ar == x)[0])
                for index, values in enumerate(indices):
                    if (index+1 <= len(indices)-1):
                        if (indices[index+1] - values) < leaves+1:
                            penalty = penalty + 10
            fitness = 1/(1 + penalty)
            fitness = penalty
            return fitness
        return function1

    def runInstance(self):
        ga_instance = pygad.GA(num_generations = self.num_generations,
                       num_parents_mating = self.num_parents_mating,
                       fitness_func = self.fitness_function,
                       sol_per_pop = self.sol_per_pop,
                       num_genes = self.num_genes,
                       gene_type = int,
                       init_range_low = self.init_range_low,
                       init_range_high = self.init_range_high,
                       parent_selection_type = self.parent_selection_type,
                       keep_parents = self.keep_parents,
                       crossover_type = self.crossover_type,
                       mutation_type = self.mutation_type,
                       gene_space = self.gene_space,
                       mutation_percent_genes = self.mutation_percent_genes
                       )
        ga_instance.run()
        return ga_instance
   