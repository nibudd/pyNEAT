import numpy as np
from copy import deepcopy
from Genotype import Genotype
import NodeGeneFactory
from NodeGene import NodeGene
from EdgeGene import EdgeGene
import StandardConfig as config

class GenotypeMutator:

    def __init__(self):
        self.node_genes = []
        self.edge_genes = []

    def mutate_genotype(self, genotype: Genotype) -> Genotype:
        genotype = self._mutate_weights(genotype)
        genotype = self._mutate_new_node(genotype)
        genotype = self._mutate_new_edge(genotype)

        return genotype

    def _mutate_weights(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)

        for edge_gene in genotype.edge_genes:
            if _get_rand() <= config.chance_of_weight_mutating:
                if _get_rand() <= config.chance_of_weight_perturbing:
                    edge_gene.weight += _randomly_perturb_weight()
                else:
                    edge_gene.weight = _randomly_reset_weight()

            if not edge_gene.enabled:
                if _get_rand() <= config.chance_of_enabling_disabled_gene:
                    edge_gene.enabled = True

        return genotype

    def _mutate_new_node(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)

        for edge_gene in genotype.edge_genes:
            if _get_rand() <= config.chance_of_adding_new_node:
                start_node = edge_gene.in_node
                end_node = edge_gene.out_node

                new_node = self._get_node_gene(edge_gene)
                new_start_edge = self._get_edge_gene(start_node, new_node, weight=1, enabled=True)
                new_end_edge = self._get_edge_gene(new_node, end_node, weight=edge_gene.weight, enabled=edge_gene.enabled)
                edge_gene.enabled = False

                genotype.node_genes.append(new_node)
                genotype.edge_genes.extend([new_start_edge, new_end_edge])

        return genotype

    def _mutate_new_edge(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)
        from_nodes = [node_gene for node_gene in genotype.node_genes if not node_gene.is_output()]
        to_nodes = [node_gene for node_gene in genotype.node_genes if not node_gene.is_input() and not node_gene.is_bias()]

        for from_node in from_nodes:
            if _get_rand() <= config.chance_of_adding_new_edge:
                valid_to_nodes = [node_gene for node_gene in to_nodes if node_gene != from_node]
                to_node = np.random.choice(valid_to_nodes)
                new_edge = self._get_edge_gene(from_node, to_node, weight=1, enabled=True)

                genotype.edge_genes.append(new_edge)

        return genotype

    def _get_node_gene(self, edge_being_split: int) -> NodeGene:
        for node_gene in self.node_genes:
            if node_gene.split_id == edge_being_split:
                return node_gene

        new_node = NodeGeneFactory.make_hidden(self._get_next_id(), edge_being_split)
        self.node_genes.append(new_node)
        return NodeGeneFactory.make_hidden(id, edge_being_split)

    def _get_edge_gene(self, in_node: NodeGene, out_node: NodeGene, weight: int, enabled: bool) -> EdgeGene:
        id = self._get_next_id()
        for edge_gene in self.edge_genes:
            if edge_gene.in_node == in_node and edge_gene.out_node == out_node:
                return edge_gene

        new_edge = EdgeGene(in_node, out_node, weight, enabled, id)
        self.edge_genes.append(new_edge)
        return new_edge

    def _get_next_id(self) -> int:
        last_edge_id = self.edge_genes[-1].id
        last_node_id = self.node_genes[-1].id
        return max(last_edge_id, last_node_id) + 1

def _get_rand() -> float:
    return np.random.rand(1)[0]

def _randomly_perturb_weight() -> float:
    return (_get_rand() * 2 * config.weight_perturbation_limit) - config.weight_perturbation_limit

def _randomly_reset_weight() -> float:
    return (_get_rand() * 2 * config.weight_reset_limit) - config.weight_reset_limit
