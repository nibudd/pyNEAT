from copy import deepcopy

from Genotype import Genotype
import XorConfiguration as config


def main():
    node_genes_0 = config.get_starting_node_genes()

    population = [
        Genotype(deepcopy(node_genes_0), []) for i in range(config.population_size)
    ]

    # calculate shared fitness of each individual
    # calculate total fitness of each species
    # kill off under-performing individuals (worse than 1 std?)
    # replace population with offspring
    # champions in large species are carried forward to next generation
    # create pool of parent candidates based on shared fitness relative to total population fitness
    # run lottery without replacement to choose a parent
    # if parent reproduces by crossover
    # if interspecies mating
    # invert compatibility_distance_threshold restriction
    # choose second parent by lottery w/o replacement
    # generate unmutated offspring
    # apply mutations
    # run until new population reaches max size


if __name__ == "__main__":
    main()
