from EdgeGene import EdgeGene
from NodeGene import NodeGene

class Genotype:

    def __init__(self, edge_genes: list[EdgeGene], node_genes: list[NodeGene]):
        self.edge_genes = edge_genes
        self.node_genes = node_genes