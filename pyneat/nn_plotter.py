from copy import deepcopy

import matplotlib.pyplot as plt

from pyneat.node import Node


class NNPlotter:
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def plot(self):
        nodes = self.nodes

        node_points = {node.id: Point(1, 1) for node in nodes}

        fig, ax = plt.subplots()

        ids_by_layer = self._sort_by_layer()

        for layer, ids in enumerate(ids_by_layer):
            for id in ids:
                node = [n for n in nodes if n.id == id][0]
                node_points[id].x += layer
                x, y = node_points[id].coordinates

                self._plot_node(ax, id, x, y)
                self._update_child_points(node_points, node)

        self._plot_edges(node_points, ax)

        plt.show()

    def _sort_by_layer(self) -> list[list[int]]:
        nodes = deepcopy(self.nodes)

        ids_by_layer = []
        while nodes:
            layer_nodes = [n for n in nodes if not n.has_parents()]
            layer_ids = [n.id for n in layer_nodes]
            ids_by_layer.append(layer_ids)

            self._unlink_nodes(layer_nodes)
            nodes = [n for n in nodes if n not in layer_nodes]

        return ids_by_layer

    def _unlink_nodes(self, layer_nodes):
        for p in layer_nodes:
            for c in p.children:
                p.unlink_child(c)

    def _update_child_points(self, node_points, node):
        for i, child in enumerate(node.children):
            node_points[child.id].y += i
            i += 1

    def _plot_node(self, ax, id, x, y):
        ax.plot(x, y, "bo", markersize=12)
        ax.text(x, y + 0.05, str(id), fontsize="large")

    def _plot_edges(self, node_points, ax):
        for node in self.nodes:
            x1, y1 = node_points[node.id].coordinates
            for child in node.children:
                x2, y2 = node_points[child.id].coordinates
                ax.plot([x1, x2], [y1, y2], "k-")
                print(x1, y1, x2, y2)


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def coordinates(self) -> tuple[float, float]:
        return (self.x, self.y)
