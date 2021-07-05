import random
from copy import deepcopy
from Genotype import Genotype
from NodeGene import NodeGene
from EdgeGene import EdgeGene
import StandardConfig as config

# todo: this should be a class which keeps track of all node and edge genes
class Mutator:

    def __init__(self, node_genes: list[NodeGene], edge_genes: list[EdgeGene]):
        self.node_genes = node_genes
        self.edge_genes = edge_genes

    def mutate_genotype(genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)
        genotype = _mutate_weights(genotype)
        genotype = _mutate_new_node(genotype)
        genotype = _mutate_new_edge(genotype)

        return genotype

    def _mutate_weights(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)
        random.seed()

        for edge_gene in genotype.edge_genes:
            if random.random() <= config.chance_of_weight_mutating:
                if random.random() <= config.chance_of_weight_perturbing:
                    # perturb weight
                else:
                    # assign new value from uniform dist.

            if not edge_gene.enabled:
                if random.random() <= config.chance_of_enabling_disabled_gene:
                    edge_gene.enabled = True
