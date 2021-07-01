import numpy as np
import pytest
from NeuralNetwork import NeuralNetwork
from NeuralNetworkRunner import run_neural_network


@pytest.mark.parametrize("outputs,expected", [
    ([1], [1]),
    ([1, 2], [1, 2]),
    ([1, 2, 3], [1, 2, 3]),
    ([1, 2, 3, 4], [1, 2, 3, 4])
])
def test_returns_correct_subarray(outputs, expected):
    n = 10
    weights = np.eye(n)
    max_iterations = 1
    nn = NeuralNetwork(weights, max_iterations, outputs)
    input = np.arange(n).reshape((n, 1))

    result = run_neural_network(nn, input)
    expected = np.array([expected]).T

    assert np.array_equal(expected, result)

@pytest.mark.parametrize("max_iterations,expected", [
    (1, [2, 3]),
    (2, [4, 9]),
    (3, [8, 27]),
    (4, [16, 81])
])
def test_runs_for_max_iterations(max_iterations, expected):
    weights = np.diag([1, 2, 3])
    outputs = [1, 2]
    nn = NeuralNetwork(weights, max_iterations, outputs)
    input = np.array([[1, 1, 1]]).T

    result = run_neural_network(nn, input)
    expected = np.array([expected]).T

    assert np.array_equal(expected, result)

def test_returns_before_max_iterations_trivial():
    weights = np.diag([0, 0, 1])
    max_iterations = 5
    outputs = [1, 2]
    nn = NeuralNetwork(weights, max_iterations, outputs)
    input = np.array([[0, 0, 1]]).T

    result = run_neural_network(nn, input)
    expected = input[outputs, :]

    assert np.array_equal(expected, result)