import numpy as np

from Genotype import Genotype
from NodeGene import BiasNodeGene, InputNodeGene, OutputNodeGene, HiddenNodeGene
from EdgeGene import EdgeGene
from PhenotypeUtility import evaluate_feedforward


def sigmoid(x):
    return 1 / (1 + np.exp(-4.9 * x))


def test_network_with_no_edges_returns_sigmoid_of_zero():
    nodes = [InputNodeGene(0), OutputNodeGene(1)]
    genotype = Genotype(nodes, [])

    inputs = np.array([1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    assert result.shape == (1, 1)
    assert np.isclose(result[0, 0], 0.5)


def test_single_input_to_output_applies_weight_and_sigmoid():
    input_node = InputNodeGene(0)
    output_node = OutputNodeGene(1)
    edge = EdgeGene(id=0, innovation_id=0, in_node=input_node, out_node=output_node, weight=1.0, enabled=True)

    genotype = Genotype([input_node, output_node], [edge])
    inputs = np.array([0.5])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    expected = sigmoid(0.5 * 1.0)
    assert np.isclose(result[0, 0], expected)


def test_bias_node_contributes_value_of_one():
    bias_node = BiasNodeGene(0)
    output_node = OutputNodeGene(1)
    edge = EdgeGene(id=0, innovation_id=0, in_node=bias_node, out_node=output_node, weight=2.0, enabled=True)

    genotype = Genotype([bias_node, output_node], [edge])
    inputs = np.array([])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    expected = sigmoid(1.0 * 2.0)
    assert np.isclose(result[0, 0], expected)


def test_disabled_edge_does_not_contribute_to_output():
    input_node = InputNodeGene(0)
    output_node = OutputNodeGene(1)
    edge = EdgeGene(id=0, innovation_id=0, in_node=input_node, out_node=output_node, weight=1.0, enabled=False)

    genotype = Genotype([input_node, output_node], [edge])
    inputs = np.array([1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    assert np.isclose(result[0, 0], 0.5)


def test_multiple_inputs_sum_weighted_contributions():
    input1 = InputNodeGene(0)
    input2 = InputNodeGene(1)
    output = OutputNodeGene(2)
    edge1 = EdgeGene(id=0, innovation_id=0, in_node=input1, out_node=output, weight=0.5, enabled=True)
    edge2 = EdgeGene(id=1, innovation_id=1, in_node=input2, out_node=output, weight=-0.5, enabled=True)

    genotype = Genotype([input1, input2, output], [edge1, edge2])
    inputs = np.array([1.0, 1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    expected = sigmoid(1.0 * 0.5 + 1.0 * -0.5)
    assert np.isclose(result[0, 0], expected)


def test_single_hidden_layer_propagates_through_two_edges():
    input_node = InputNodeGene(0)
    hidden_node = HiddenNodeGene(1)
    output_node = OutputNodeGene(2)

    edge1 = EdgeGene(id=0, innovation_id=0, in_node=input_node, out_node=hidden_node, weight=1.0, enabled=True)
    edge2 = EdgeGene(id=1, innovation_id=1, in_node=hidden_node, out_node=output_node, weight=1.0, enabled=True)

    genotype = Genotype([input_node, hidden_node, output_node], [edge1, edge2])
    inputs = np.array([1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    hidden_value = sigmoid(1.0 * 1.0)
    expected = sigmoid(hidden_value * 1.0)
    assert np.isclose(result[0, 0], expected)


def test_two_hidden_layers_propagate_sequentially():
    input_node = InputNodeGene(0)
    hidden1 = HiddenNodeGene(1)
    hidden2 = HiddenNodeGene(2)
    output_node = OutputNodeGene(3)

    edge1 = EdgeGene(id=0, innovation_id=0, in_node=input_node, out_node=hidden1, weight=1.0, enabled=True)
    edge2 = EdgeGene(id=1, innovation_id=1, in_node=hidden1, out_node=hidden2, weight=1.0, enabled=True)
    edge3 = EdgeGene(id=2, innovation_id=2, in_node=hidden2, out_node=output_node, weight=1.0, enabled=True)

    genotype = Genotype([input_node, hidden1, hidden2, output_node], [edge1, edge2, edge3])
    inputs = np.array([1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    h1_value = sigmoid(1.0)
    h2_value = sigmoid(h1_value)
    expected = sigmoid(h2_value)
    assert np.isclose(result[0, 0], expected)


def test_scrambled_node_order_still_evaluates_correctly():
    input_node = InputNodeGene(0)
    hidden1 = HiddenNodeGene(1)
    hidden2 = HiddenNodeGene(2)
    output_node = OutputNodeGene(3)

    edge1 = EdgeGene(id=0, innovation_id=0, in_node=input_node, out_node=hidden1, weight=1.0, enabled=True)
    edge2 = EdgeGene(id=1, innovation_id=1, in_node=hidden1, out_node=hidden2, weight=1.0, enabled=True)
    edge3 = EdgeGene(id=2, innovation_id=2, in_node=hidden2, out_node=output_node, weight=1.0, enabled=True)

    genotype = Genotype([output_node, hidden2, input_node, hidden1], [edge1, edge2, edge3])
    inputs = np.array([1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    h1_value = sigmoid(1.0)
    h2_value = sigmoid(h1_value)
    expected = sigmoid(h2_value)
    assert np.isclose(result[0, 0], expected)


def test_diamond_topology_merges_parallel_paths():
    input_node = InputNodeGene(0)
    hidden1 = HiddenNodeGene(1)
    hidden2 = HiddenNodeGene(2)
    output_node = OutputNodeGene(3)

    edge1 = EdgeGene(id=0, innovation_id=0, in_node=input_node, out_node=hidden1, weight=1.0, enabled=True)
    edge2 = EdgeGene(id=1, innovation_id=1, in_node=input_node, out_node=hidden2, weight=1.0, enabled=True)
    edge3 = EdgeGene(id=2, innovation_id=2, in_node=hidden1, out_node=output_node, weight=0.5, enabled=True)
    edge4 = EdgeGene(id=3, innovation_id=3, in_node=hidden2, out_node=output_node, weight=0.5, enabled=True)

    genotype = Genotype([input_node, hidden1, hidden2, output_node], [edge1, edge2, edge3, edge4])
    inputs = np.array([1.0])
    result = evaluate_feedforward(genotype, inputs, sigmoid)

    h1_value = sigmoid(1.0)
    h2_value = sigmoid(1.0)
    expected = sigmoid(h1_value * 0.5 + h2_value * 0.5)
    assert np.isclose(result[0, 0], expected)
