import numpy as np
from NeuralNetwork import NeuralNetwork

def run_neural_network(neural_network: NeuralNetwork, input: np.array) -> np.array:
    x = np.copy(input)
    W = neural_network.weights

    for i in range(neural_network.max_iterations):
        y = W @ x

        if _array_is_zero(y):
            y = x
            break

        x = y

    return y[neural_network.outputs, :]


def _array_is_zero(x: np.array) -> bool:
    return np.count_nonzero(x) == 0