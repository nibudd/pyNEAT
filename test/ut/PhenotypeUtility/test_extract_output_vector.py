import numpy as np
import NodeGeneFactory
from PhenotypeUtility import extract_output_vector


def test_returns_outputs():
    input_1 = NodeGeneFactory.make_input(0)
    input_2 = NodeGeneFactory.make_input(1)
    output_1 = NodeGeneFactory.make_output(2)
    hidden_1 = NodeGeneFactory.make_hidden(3, 0)
    node_genes = [input_1, input_2, output_1, hidden_1]

    nn_outputs = np.array([[1, 2, 3, 4]]).T
    outputs = extract_output_vector(node_genes, nn_outputs)
    expected = np.array([[3]]).T

    assert np.array_equal(expected, outputs)
