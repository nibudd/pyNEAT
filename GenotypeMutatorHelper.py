import random

import NodeGeneFactory
from EdgeGene import EdgeGene
from NodeGene import NodeGene
from StandardConfig import StandardConfig


class GenotypeMutatorHelper:

    def __init__(self, config: StandardConfig, last_gene_id: int):
        self.config = config
        self.last_gene_id = last_gene_id
        self.edge_genes = []
        self.node_genes = []

    def weight_is_mutating(self, rand: float) -> bool:
        return rand <= self.config.chance_of_weight_mutating

    def weight_is_perturbing(self, rand: float) -> bool:
        return rand <= self.config.chance_of_weight_perturbing

    def gene_is_reenabling(self, rand: float) -> bool:
        return rand <= self.config.chance_of_enabling_disabled_gene

    def edge_is_splitting(self, rand: float) -> bool:
        return rand <= self.config.chance_of_adding_new_node

    def new_edge_is_being_added(self, rand: float) -> bool:
        return rand <= self.config.chance_of_adding_new_edge

    def perturb_weight(self, rand: float) -> float:
        return rand * 2 * self.config.weight_perturbation_limit - self.config.weight_perturbation_limit

    def reset_weight(self, rand: float) -> float:
        return rand * 2 * self.config.weight_reset_limit - self.config.weight_reset_limit

    def get_node_gene_from_edge(self, edge_being_split: EdgeGene) -> NodeGene:
        for node_gene in self.node_genes:
            if node_gene.split_id == edge_being_split:
                return node_gene

        new_node = NodeGeneFactory.make_hidden(self._increment_gene_id(), edge_being_split.id)
        self.node_genes.append(new_node)
        return new_node

    def get_edge_gene_from_nodes(self, in_node: NodeGene, out_node: NodeGene, weight: int=1, enabled: bool=True) -> EdgeGene:
        for edge_gene in self.edge_genes:
            if edge_gene.in_node == in_node and edge_gene.out_node == out_node:
                return edge_gene

        new_edge = EdgeGene(in_node, out_node, weight, enabled, self._increment_gene_id())
        self.edge_genes.append(new_edge)
        return new_edge

    def _increment_gene_id(self) -> int:
        self.last_gene_id += 1
        return self.last_gene_id
