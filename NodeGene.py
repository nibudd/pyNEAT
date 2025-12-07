from abc import ABC, abstractmethod


class NodeGene(ABC):

    def __init__(self, id: int):
        self.id = id

    def is_bias(self) -> bool:
        return False

    def is_input(self) -> bool:
        return False

    def is_output(self) -> bool:
        return False


class BiasNodeGene(NodeGene):
    def is_bias(self) -> bool:
        return True


class InputNodeGene(NodeGene):
    def is_input(self) -> bool:
        return True


class OutputNodeGene(NodeGene):
    def is_output(self) -> bool:
        return True


class HiddenNodeGene(NodeGene):
    pass
