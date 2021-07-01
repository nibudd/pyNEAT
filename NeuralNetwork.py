import numpy as np


class NeuralNetwork:

    def __init__(self, weights: np.array, max_iterations: int, outputs: list[int]):
        self.weights = weights
        self.max_iterations = max_iterations
        self.outputs = outputs