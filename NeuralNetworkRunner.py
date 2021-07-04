import numpy as np

def run_neural_network(weights: np.array, input: np.array) -> np.array:
    x = np.copy(input)
    W = weights
    max_iterations = 100
    iteration_count = 0

    while iteration_count < max_iterations:
        iteration_count += 1

        y = W @ x
        y = 1 / (1 + np.exp(-4.9 * y))

        if np.equal(y, x).all():
            y = x
            break

        x = y

    return y
