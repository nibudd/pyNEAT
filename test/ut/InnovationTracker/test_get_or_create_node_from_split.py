from InnovationTracker import InnovationTracker
from NodeGene import InputNodeGene, OutputNodeGene, HiddenNodeGene
from EdgeGene import EdgeGene


def test_first_call_creates_new_node_with_incremented_id():
    tracker = InnovationTracker(last_node_id=3, last_edge_id=0, last_innovation_id=0)
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    edge = EdgeGene(
        id=0,
        innovation_id=0,
        in_node=in_node,
        out_node=out_node,
        weight=1.0,
        enabled=True,
    )

    node = tracker.get_or_create_node_from_split(edge)

    assert isinstance(node, HiddenNodeGene)
    assert node.id == 4
    assert tracker.last_node_id == 4


def test_second_call_with_same_edge_returns_same_node():
    tracker = InnovationTracker(last_node_id=3, last_edge_id=0, last_innovation_id=0)
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    edge = EdgeGene(
        id=0,
        innovation_id=0,
        in_node=in_node,
        out_node=out_node,
        weight=1.0,
        enabled=True,
    )

    node1 = tracker.get_or_create_node_from_split(edge)
    node2 = tracker.get_or_create_node_from_split(edge)

    assert node1 is node2
    assert tracker.last_node_id == 4


def test_different_edges_return_different_nodes():
    tracker = InnovationTracker(last_node_id=3, last_edge_id=1, last_innovation_id=1)
    in_node = InputNodeGene(0)
    out_node = OutputNodeGene(1)
    edge1 = EdgeGene(
        id=0,
        innovation_id=0,
        in_node=in_node,
        out_node=out_node,
        weight=1.0,
        enabled=True,
    )
    edge2 = EdgeGene(
        id=1,
        innovation_id=1,
        in_node=in_node,
        out_node=out_node,
        weight=0.5,
        enabled=True,
    )

    node1 = tracker.get_or_create_node_from_split(edge1)
    node2 = tracker.get_or_create_node_from_split(edge2)

    assert node1.id == 4
    assert node2.id == 5
    assert node1 is not node2
    assert tracker.last_node_id == 5
