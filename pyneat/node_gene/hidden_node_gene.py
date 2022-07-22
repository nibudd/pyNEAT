from .node_gene import NodeGene


class HiddenNodeGene(NodeGene):
    def __init__(self, id: int):
        super().__init__(id)
