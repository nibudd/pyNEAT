import numpy as np

# general values
population_size = 150
transfer_function = lambda x: 1 / (1 + np.exp(-4.9 * x))

# species values
coefficient_excess = 1.0
coefficient_disjoint = 1.0
coefficient_avg_weights = 0.4
compatibility_distance_threshold = 3.0
max_generations_to_improve = 15
min_species_size_to_copy_champion_forward = 6

# mutation values
chance_of_weight_mutating = 0.8
chance_of_weight_perturbing = 0.9 # if not perturbed, weight is assigned new uniform random value
chance_of_enabling_disabled_gene = 0.25
chance_of_adding_new_node = 0.03
chance_of_adding_new_edge = 0.05
weight_perturbation_limit = 2.5
weight_reset_limit = 2.5

# mating values
fraction_of_offspring_from_budding = 0.25
interspecies_mating_rate = 0.001
