from copy import deepcopy
import random

from EdgeGene import EdgeGene
from Genotype import Genotype
from NodeGene import NodeGene
from StandardConfig import StandardConfig


class GenotypeMutator:

    def __init__(self, genotype: Genotype, config: type[StandardConfig]):
        self.genotype = genotype
        self._sync_ids_from_genotype(genotype)
        self.config = config
        random.seed()

    def mutate_genotype(self, genotype: Genotype) -> Genotype:
        genotype = self._mutate_weights(self.genotype)
        genotype = self._mutate_new_node(genotype)
        genotype = self._mutate_new_edge(genotype)

        self.genotype = genotype
        return genotype

    def _mutate_weights(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)

        for edge_gene in genotype.edge_genes:
            if self._weight_is_mutating(random.random()):
                if self._weight_is_perturbing(random.random()):
                    edge_gene.weight += self._perturb_weight(random.random())
                else:
                    edge_gene.weight = self._reset_weight(random.random())

            if not edge_gene.enabled:
                if self._gene_is_reenabling(random.random()):
                    edge_gene.enabled = True

        return genotype

    def _mutate_new_node(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)

        for edge_gene in genotype.edge_genes:
            if self._edge_is_splitting(random.random()):
                start_node = edge_gene.in_node
                end_node = edge_gene.out_node

                new_node = self._get_node_gene_from_edge(edge_gene)
                new_start_edge = self._get_edge_gene_from_nodes(start_node, new_node)
                new_end_edge = self._get_edge_gene_from_nodes(
                    new_node, end_node, edge_gene.weight, edge_gene.enabled
                )
                edge_gene.enabled = False

                genotype.node_genes.append(new_node)
                genotype.edge_genes.extend([new_start_edge, new_end_edge])

        return genotype

    def _mutate_new_edge(self, genotype: Genotype) -> Genotype:
        genotype = deepcopy(genotype)
        from_nodes = [
            node_gene for node_gene in genotype.node_genes if not node_gene.is_output()
        ]
        to_nodes = [
            node_gene
            for node_gene in genotype.node_genes
            if not node_gene.is_input() and not node_gene.is_bias()
        ]

        for from_node in from_nodes:
            if self._new_edge_is_being_added(random.random()):
                valid_to_nodes = [
                    node_gene for node_gene in to_nodes if node_gene != from_node
                ]
                to_node = random.choice(valid_to_nodes)
                new_edge = self._get_edge_gene_from_nodes(from_node, to_node)

                genotype.edge_genes.append(new_edge)

        return genotype

    def _weight_is_mutating(self, rand: float) -> bool:
        return rand <= self.config.chance_of_weight_mutating

    def _weight_is_perturbing(self, rand: float) -> bool:
        return rand <= self.config.chance_of_weight_perturbing

    def _gene_is_reenabling(self, rand: float) -> bool:
        return rand <= self.config.chance_of_enabling_disabled_gene

    def _edge_is_splitting(self, rand: float) -> bool:
        return rand <= self.config.chance_of_adding_new_node

    def _new_edge_is_being_added(self, rand: float) -> bool:
        return rand <= self.config.chance_of_adding_new_edge

    def _perturb_weight(self, rand: float) -> float:
        return (
            rand * 2 * self.config.weight_perturbation_limit
            - self.config.weight_perturbation_limit
        )

    def _reset_weight(self, rand: float) -> float:
        return (
            rand * 2 * self.config.weight_reset_limit - self.config.weight_reset_limit
        )

    # def _get_node_gene_from_edge(self, edge_being_split: EdgeGene) -> NodeGene:
    #     for node_gene in self.genotype.node_genes:
    #         if node_gene.split_id == edge_being_split:
    #             return node_gene
    #
    #     new_node = NodeGeneFactory.make_hidden(self._increment_gene_id(), edge_being_split.edge_id)
    #     self.node_genes.append(new_node)
    #     return new_node
    #
    # def _get_edge_gene_from_nodes(self, in_node: NodeGene, out_node: NodeGene, weight: int=1, enabled: bool=True) -> EdgeGene:
    #     for edge_gene in self.edge_genes:
    #         if edge_gene.in_node == in_node and edge_gene.out_node == out_node:
    #             return edge_gene
    #
    #     new_edge = EdgeGene(in_node, out_node, weight, enabled, self._increment_gene_id())
    #     self.edge_genes.append(new_edge)
    #     return new_edge

    def _sync_ids_from_genotype(self, genotype: Genotype):
        if genotype.node_genes:
            self.last_node_id = max(node_gene.id for node_gene in genotype.node_genes)
        else:
            self.last_node_id = 0

        if genotype.edge_genes:
            self.last_edge_id = max(edge_gene.id for edge_gene in genotype.edge_genes)
            self.last_innovation_id = max(
                edge_gene.innovation_id for edge_gene in genotype.edge_genes
            )
        else:
            self.last_edge_id = 0
            self.last_innovation_id = 0
