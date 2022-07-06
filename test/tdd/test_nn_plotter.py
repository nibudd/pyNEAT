from pyneat.nn_plotter import NNPlotter
from pyneat.node import Node


def test_simple_neural_network_plot():
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    n1.add_child(n2)
    n1.add_child(n3)
    n1.add_child(n5)
    n2.add_child(n3)
    n2.add_child(n4)
    n2.add_child(n6)
    n3.add_child(n4)
    n5.add_child(n3)
    n5.add_child(n6)
    n6.add_child(n4)

    nodes = [n1, n2, n3, n4, n5, n6]
    plotter = NNPlotter(nodes)
    plotter.plot()
