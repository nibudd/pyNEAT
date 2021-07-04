import numpy as np


class NeuralNetwork:

    def __init__(self, weights: np.array, outputs: list[int]):
        self.weights = weights
        self.outputs = outputs