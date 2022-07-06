from copy import deepcopy
from Genotype import Genotype
from NodeGene import NodeGene
from EdgeGene import EdgeGene
from GenotypeMutatorHelper import GenotypeMutatorHelper
from StandardConfig import StandardConfig


class GenotypeMutator:

    def __init__(self, config: StandardConfig, last_gene_id: int, randomizer: object):
        self.helper = GenotypeMutatorHelper(config, last_gene_id)

    def mutate_genotype(self, genotype: Genotype) -> Genotype:
        genotype = self._mutate_weights(genotype)
        genotype = self._mutate_new_node(genotype)
        genotype = self._mutate_new_edge(genotype)

        return genotype

    def _mutate_weights(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)

        for edge_gene in genotype.edge_genes:
            if self.helper.weight_is_mutating(self.randomizer.random()):
                if self.helper.weight_is_perturbing(self.randomizer.random()):
                    edge_gene.weight += self.helper.perturb_weight(self.randomizer.random())
                else:
                    edge_gene.weight = self.helper.reset_weight(self.randomizer.random())

            if not edge_gene.enabled:
                if self.helper.gene_is_reenabling(self.randomizer.random()):
                    edge_gene.enabled = True

        return genotype

    def _mutate_new_node(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)

        for edge_gene in genotype.edge_genes:
            if self.helper.edge_is_splitting(self.randomizer.random()):
                start_node = edge_gene.in_node
                end_node = edge_gene.out_node

                new_node = self.helper.get_node_gene_from_edge(edge_gene)
                new_start_edge = self.helper.get_edge_gene_from_nodes(start_node, new_node)
                new_end_edge = self.helper.get_edge_gene_from_nodes(new_node, end_node, edge_gene.weight, edge_gene.enabled)
                edge_gene.enabled = False

                genotype.node_genes.append(new_node)
                genotype.edge_genes.extend([new_start_edge, new_end_edge])

        return genotype

    def _mutate_new_edge(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)
        from_nodes = [node_gene for node_gene in genotype.node_genes if not node_gene.is_output()]
        to_nodes = [node_gene for node_gene in genotype.node_genes if not node_gene.is_input() and not node_gene.is_bias()]

        for from_node in from_nodes:
            if self.helper.new_edge_is_being_added(self.randomizer.random()):
                valid_to_nodes = [node_gene for node_gene in to_nodes if node_gene != from_node]
                to_node = self.randomizer.choice(valid_to_nodes)
                new_edge = self.helper.get_edge_gene_from_nodes(from_node, to_node)

                genotype.edge_genes.append(new_edge)

        return genotype
