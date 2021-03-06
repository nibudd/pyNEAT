from NodeGene import NodeGene


class EdgeGene:

    def __init__(self, in_node: NodeGene, out_node: NodeGene, weight: float, enabled: bool, edge_id: int):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.edge_id = edge_id
