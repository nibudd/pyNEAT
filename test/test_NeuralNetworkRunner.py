import numpy as np
from StandardConfig import transfer_function
from NeuralNetworkRunner import NeuralNetworkRunner


def test_returns_correct_output():
    weights = np.array([[100, 0, 0, 0, 0],
                        [0, 100, 0, 0, 0],
                        [0, 0, 100, 0, 0],
                        [.1, 0, .2, 0, .5],
                        [.2, .3, 0, .4, 0]])

    input = np.array([[1, 1, 1, 0, 0]]).T

    nn_runner = NeuralNetworkRunner(transfer_function)
    result = nn_runner.run(weights, input)
    expected = np.array([[1, 1, 1, 0.97995276, 0.98751554]]).T

    assert np.allclose(expected, result)