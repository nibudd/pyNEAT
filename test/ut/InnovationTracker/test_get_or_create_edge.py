from InnovationTracker import InnovationTracker
from NodeGene import InputNodeGene, OutputNodeGene
from EdgeGene import EdgeGene


def test_first_call_creates_new_edge_with_incremented_ids():
    tracker = InnovationTracker(last_node_id=3, last_edge_id=0, last_innovation_id=0)
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)

    edge = tracker.get_or_create_edge(in_node, out_node, weight=0.5, enabled=True)

    assert isinstance(edge, EdgeGene)
    assert edge.id == 1
    assert edge.innovation_id == 1
    assert edge.in_node is in_node
    assert edge.out_node is out_node
    assert edge.weight == 0.5
    assert edge.enabled is True
    assert tracker.last_edge_id == 1
    assert tracker.last_innovation_id == 1


def test_second_call_with_same_nodes_returns_edge_with_same_ids():
    tracker = InnovationTracker(last_node_id=3, last_edge_id=0, last_innovation_id=0)
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)

    edge1 = tracker.get_or_create_edge(in_node, out_node, weight=0.5, enabled=True)
    edge2 = tracker.get_or_create_edge(in_node, out_node, weight=-0.3, enabled=False)

    assert edge1.id == edge2.id
    assert edge1.innovation_id == edge2.innovation_id
    assert edge2.weight == -0.3
    assert edge2.enabled is False
    assert tracker.last_edge_id == 1
    assert tracker.last_innovation_id == 1


def test_different_node_pairs_return_edges_with_different_ids():
    tracker = InnovationTracker(last_node_id=3, last_edge_id=0, last_innovation_id=0)
    in_node1 = InputNodeGene(0)
    in_node2 = InputNodeGene(1)
    out_node = OutputNodeGene(2)

    edge1 = tracker.get_or_create_edge(in_node1, out_node, weight=0.5, enabled=True)
    edge2 = tracker.get_or_create_edge(in_node2, out_node, weight=0.5, enabled=True)

    assert edge1.id == 1
    assert edge1.innovation_id == 1
    assert edge2.id == 2
    assert edge2.innovation_id == 2
    assert tracker.last_edge_id == 2
    assert tracker.last_innovation_id == 2
