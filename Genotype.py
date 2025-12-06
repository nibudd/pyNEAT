from EdgeGene import EdgeGene
from NodeGene import NodeGene


class Genotype:
    def __init__(self, node_genes: list[NodeGene], edge_genes: list[EdgeGene]):
        self.edge_genes = edge_genes
        self.node_genes = node_genes
