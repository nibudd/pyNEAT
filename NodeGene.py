from NodeType import NodeType

class NodeGene:

    def __init__(self, node_type: NodeType, id: int):
        self.type = node_type
        self.id = id

    def is_input(self) -> bool:
        return self.type.is_input()