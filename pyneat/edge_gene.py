from node_gene import NodeGene


class EdgeGene:
    def __init__(
        self,
        innovation: int,
        in_node: NodeGene,
        out_node: NodeGene,
        weight: float,
        enabled: bool,
    ):
        self.innovation = innovation
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
