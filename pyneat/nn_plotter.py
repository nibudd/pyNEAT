from copy import deepcopy

import matplotlib.pyplot as plt

from pyneat.node import Node

class NNPlotter:
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def plot(self):
        nodes = deepcopy(self.nodes)

        node_locations = {
            node.id: [1, 1]
            for node in nodes
        }

        fig, ax = plt.subplots()

        layer = 0
        while nodes:
            layer_nodes = [n for n in nodes if not n.has_parents()]
            
            for node in layer_nodes:
                id = node.id
                node_locations[id][0] += layer
                x, y = node_locations[id]
                
                self._plot_node(ax, id, x, y)
                self._update_children(node_locations, node)

            self._unlink_nodes(layer_nodes)

            nodes = [n for n in nodes if n not in layer_nodes]
            layer += 1

        self._plot_edges(node_locations, ax)
                
        plt.show() 

    def _update_children(self, node_locations, node):
        for i, child in enumerate(node.children):
            node_locations[child.id][1] += i
            i += 1

    def _plot_node(self, ax, id, x, y):
        ax.plot(x, y, "bo", markersize=12)
        ax.text(x, y + .05, str(id), fontsize="large")

    def _unlink_nodes(self, layer_nodes):
        for p in layer_nodes:
            for c in p.children:
                p.unlink_child(c)

    def _plot_edges(self, node_locations, ax):
        nodes = deepcopy(self.nodes)
        for node in nodes:
            x1, y1 = node_locations[node.id]
            for child in node.children:
                x2, y2 = node_locations[child.id]
                ax.plot([x1, x2], [y1, y2], "k-")
                print(x1, y1, x2, y2)
