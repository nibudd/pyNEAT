import numpy as np
import pytest
from NeuralNetwork import NeuralNetwork
from NeuralNetworkRunner import run_neural_network


def test_returns_correct_subarray_single_output():
    weights = np.array([[100, 0, 0, 0, 0],
                        [0, 100, 0, 0, 0],
                        [0, 0, 100, 0, 0],
                        [.1, 0, .2, 0, .5],
                        [.2, .3, 0, .4, 0]])

    nn = NeuralNetwork(weights, [4])
    input = np.array([[1, 2, 3, 0, 0]]).T

    result = run_neural_network(nn, input)
    expected = np.array([[0.98751554]])

    assert np.allclose(expected, result)