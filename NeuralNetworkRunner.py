from collections.abc import Callable

import numpy as np


class NeuralNetworkRunner:

    def __init__(self, transfer_function: Callable[np.array, np.array]):
        self.transfer_function = transfer_function

    def run(self, weights: np.array, input: np.array) -> np.array:
        x = np.copy(input)
        W = weights
        max_iterations = 100
        iteration_count = 0

        while iteration_count < max_iterations:
            iteration_count += 1

            y = W @ x
            y = self.transfer_function(y)

            if np.equal(y, x).all():
                y = x
                break

            x = y

        return y
