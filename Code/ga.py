"""
	Generic Gentic Optimization Class

	Written By Rahul Kejriwal
	Started on 1/3/16
"""


from random import shuffle, randint, random
from numpy.random import choice
# from tqdm import tqdm

# for flushing stdout
from sys import stdout


"""
	Class that runs generic Genetic Optimization

	Takes an input class with following functions defined:
		
		fitness()   - returns a value proportional to caller objects fitness
		mutate()    - returns mutated version of caller object
		crossover() - static method, returns an array of crossovered offspring
"""
class GeneticOptimization:

	"""
		Initialize and Confugure GA instance
	"""
	def __init__(self, optClass, object_generator):
		self.optimizationClass = optClass
		self.object_generator  = object_generator
	
		# GA Parameters - statically defined
		self.n = 200
		self.k = 100
		self.mutate_prob = 0.4
		self.number_of_iterations = 50


	"""
		Create a starting population
	"""
	def initPopulation(self):
		population = []
		for i in range(self.n):
			population.append(self.object_generator())

		return population


	"""
		Computes Fitness for each Population Citizen
	"""
	def getFitness(self, population):
		fitness = []
		for p in population:
			fitness.append(p.fitness())

		return fitness


	"""
		Selects fitter citizens from a population
	"""
	def selection(self, population, fitness):
		selected = []

		# Compute probablilty of survival of citizen 
		total_fitness = sum(fitness)
		for i in range(len(fitness)):
			fitness[i] = (fitness[i]*1.0) / total_fitness

		# Select individuals
		for i in range(self.n):
			t =  choice(range(self.n), p=fitness)
			selected.append(population[t])

		return selected


	"""
		Creates a CrossOverEd Population from selevted individuals
	"""
	def crossoverPopulation(self, population):
		offspring = []

		shuffle(population)
		parent_1 = population[:len(population)/2]
		parent_2 = population[len(population)/2:]

		for i in range(len(parent_1)):
			offspring += self.optimizationClass.crossover(parent_1[i], parent_2[i])

		return offspring


	"""
		Creates a mutated Population
	"""
	def mutate(self, population):
		mutation = []
		for p in population: 
			if random() <= self.mutate_prob:
				mutation.append(p.mutate())
			else:
				mutation.append(p)

		return mutation


	"""
		Optimize Population from GenX + GenY
	"""
	def optimizePopulation(self, original_population, derived_population, fitness):
		orig_sorted = [x for (y,x) in sorted(zip(fitness, original_population))]
		derv_sorted = sorted(derived_population, key = lambda x: x.fitness())

		return derv_sorted[-self.k:] + orig_sorted[self.k:]


	"""
		Get the ultimate best from population
	"""
	def best(self, population):
		best_individual = population[0]
		best_fitness    = best_individual.fitness()
		
		for i in range(1, self.n):
			curr_fitness = population[i].fitness()
			if curr_fitness < best_fitness:
				best_fitness, best_individual = curr_fitness, population[i]

		return best_individual


	"""
		Run the GA Optimization
	"""
	def run(self):
		population = self.initPopulation()

		for i in range(self.number_of_iterations):
			population_fitness  	= self.getFitness(population)
			selected_population		= self.selection(population, population_fitness)
			offspring_population	= self.crossoverPopulation(selected_population)
			mutated_population		= self.mutate(offspring_population)
			optimal_population  	= self.optimizePopulation(population, mutated_population, population_fitness)
			
			population = optimal_population

			# Print best each iteration
			print "Iteration i: ", self.best(population).fitness()
			stdout.flush()
	
		return self.best(population)