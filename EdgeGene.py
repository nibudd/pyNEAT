from NodeGene import NodeGene


class EdgeGene:
    def __init__(
        self,
        id: int,
        innovation_id: int,
        in_node: NodeGene,
        out_node: NodeGene,
        weight: float,
        enabled: bool,
    ):
        self.id = id
        self.innovation_id = innovation_id
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
