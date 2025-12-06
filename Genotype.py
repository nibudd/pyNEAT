from EdgeGene import EdgeGene
from NodeGene import NodeGene


class Genotype:
    def __init__(self, node_genes: list[NodeGene], edge_genes: list[EdgeGene]):
        self.edge_genes = edge_genes
        self.node_genes = node_genes

    def describe(self) -> str:
        lines = ["Network Connection Table:"]
        lines.append(f"{'From Node':<12} {'To Node':<12} {'Weight':<10} {'Enabled':<8} {'Innovation ID':<15}")
        lines.append("-" * 57)
        
        for edge in self.edge_genes:
            from_id = str(edge.in_node.id)
            to_id = str(edge.out_node.id)
            weight = f"{edge.weight:.4f}"
            enabled = "Yes" if edge.enabled else "No"
            innovation_id = str(edge.innovation_id)
            lines.append(f"{from_id:<12} {to_id:<12} {weight:<10} {enabled:<8} {innovation_id:<15}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    from NodeGene import InputNodeGene, OutputNodeGene

    node1 = InputNodeGene(1)
    node2 = OutputNodeGene(2)
    edge1 = EdgeGene(1, 1, node1, node2, 0.5, True)
    edge2 = EdgeGene(2, 2, node1, node2, -1.2, False)

    genotype = Genotype([node1, node2], [edge1, edge2])
    print(genotype.describe())
