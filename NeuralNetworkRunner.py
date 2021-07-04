from collections import Callable

import numpy as np

def run_neural_network(weights: np.array, input: np.array, transfer_function: Callable[np.array, np.array]) -> np.array:
    x = np.copy(input)
    W = weights
    max_iterations = 100
    iteration_count = 0

    while iteration_count < max_iterations:
        iteration_count += 1

        y = W @ x
        y = transfer_function(y)

        if np.equal(y, x).all():
            y = x
            break

        x = y

    return y
