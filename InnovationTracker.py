from EdgeGene import EdgeGene
from NodeGene import NodeGene, HiddenNodeGene


class InnovationTracker:
    def __init__(self, last_node_id: int, last_edge_id: int, last_innovation_id: int):
        self.last_node_id = last_node_id
        self.last_edge_id = last_edge_id
        self.last_innovation_id = last_innovation_id
        self.in_out_node_ids_to_innovated_edge: dict[tuple[int, int], EdgeGene] = {}
        self.edge_id_to_innovated_node: dict[int, HiddenNodeGene] = {}

    def get_or_create_node_from_split(self, edge: EdgeGene) -> HiddenNodeGene:
        if edge.id in self.edge_id_to_innovated_node:
            return self.edge_id_to_innovated_node[edge.id]

        self.last_node_id += 1
        new_node = HiddenNodeGene(self.last_node_id)
        self.edge_id_to_innovated_node[edge.id] = new_node
        return new_node

    def get_or_create_edge(
        self,
        in_node: NodeGene,
        out_node: NodeGene,
        weight: float = 1.0,
        enabled: bool = True,
    ) -> EdgeGene:
        key = (in_node.id, out_node.id)
        if key in self.in_out_node_ids_to_innovated_edge:
            existing = self.in_out_node_ids_to_innovated_edge[key]
            return EdgeGene(
                existing.id, existing.innovation_id, in_node, out_node, weight, enabled
            )

        self.last_edge_id += 1
        self.last_innovation_id += 1
        new_edge = EdgeGene(
            self.last_edge_id,
            self.last_innovation_id,
            in_node,
            out_node,
            weight,
            enabled,
        )
        self.in_out_node_ids_to_innovated_edge[key] = new_edge
        return new_edge
