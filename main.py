import numpy as np
from Genotype import Genotype
from PhenotypeUtility import construct_weights_matrix, construct_input_vector, extract_output_vector
from NeuralNetworkRunner import run_neural_network
import XorConfiguration as config


def main():
    node_genes_0 = config.get_starting_node_genes()

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