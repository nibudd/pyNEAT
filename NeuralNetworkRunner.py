import numpy as np
from NeuralNetwork import NeuralNetwork

def run_neural_network(neural_network: NeuralNetwork, input: np.array) -> np.array:
    x = np.copy(input)
    W = neural_network.weights
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

    return y[neural_network.outputs, :]
