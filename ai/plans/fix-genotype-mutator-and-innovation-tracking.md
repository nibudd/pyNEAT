# Plan: Fix GenotypeMutator and Add Innovation Tracking

## Goal
Fix broken mutation methods in GenotypeMutator and implement proper innovation tracking for historical markings (NEAT's key innovation).

## Problems to Fix

1. **`_get_node_gene_from_edge()` and `_get_edge_gene_from_nodes()` are commented out** - code will crash if mutations trigger
2. **References removed `NodeGeneFactory`** - need to use `HiddenNodeGene` directly
3. **Wrong attribute names** - `split_id`, `edge_id` don't exist
4. **`mutate_genotype()` ignores its parameter** - uses `self.genotype` instead of passed `genotype`
5. **No global innovation tracking** - same structural mutation in different genomes should get same innovation number

## Design: Innovation Tracker

Create a new class to track innovations across the population within a generation. **Reset between generations** - same mutation in different generations gets different innovation numbers (per NEAT paper).

```python
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

    def get_or_create_edge(self, in_node: NodeGene, out_node: NodeGene,
                           weight: float = 1.0, enabled: bool = True) -> EdgeGene:
        key = (in_node.id, out_node.id)
        if key in self.in_out_node_ids_to_innovated_edge:
            existing = self.in_out_node_ids_to_innovated_edge[key]
            # Return copy with potentially different weight/enabled
            return EdgeGene(existing.id, existing.innovation_id,
                          in_node, out_node, weight, enabled)

        self.last_edge_id += 1
        self.last_innovation_id += 1
        new_edge = EdgeGene(self.last_edge_id, self.last_innovation_id,
                           in_node, out_node, weight, enabled)
        self.in_out_node_ids_to_innovated_edge[key] = new_edge
        return new_edge
```

## Files to Modify

### 1. Create `/home/nibudd/dev/pyNEAT/InnovationTracker.py`
New file with `InnovationTracker` class as shown above.

### 2. Modify `/home/nibudd/dev/pyNEAT/GenotypeMutator.py`

**Changes:**
- Remove ID tracking from GenotypeMutator (move to InnovationTracker)
- Accept `InnovationTracker` in constructor instead of tracking IDs locally
- Fix `mutate_genotype()` to use its parameter
- Uncomment and fix `_get_node_gene_from_edge()` to use tracker
- Uncomment and fix `_get_edge_gene_from_nodes()` to use tracker
- Update imports to include `HiddenNodeGene`

**New signature:**
```python
class GenotypeMutator:
    def __init__(self, config: type[StandardConfig], tracker: InnovationTracker):
        self.config = config
        self.tracker = tracker

    def mutate_genotype(self, genotype: Genotype) -> Genotype:
        genotype = self._mutate_weights(genotype)  # Fix: use parameter
        genotype = self._mutate_new_node(genotype)
        genotype = self._mutate_new_edge(genotype)
        return genotype
```

### 3. Modify `/home/nibudd/dev/pyNEAT/NodeGene.py`
No changes needed - `HiddenNodeGene` already exists.

### 4. Update tests in `/home/nibudd/dev/pyNEAT/test/ut/GenotypeMutator/`
- Update `test_sync_ids_from_genotype.py` - these tests may need adjustment or removal since ID tracking moves to InnovationTracker
- Create new test files for mutation methods

## Implementation Steps

1. **Create `InnovationTracker.py`** with the class above
2. **Write tests for InnovationTracker** - test get_or_create methods return same objects for same inputs
3. **Update GenotypeMutator** - remove ID tracking, accept tracker, fix methods
4. **Update existing GenotypeMutator tests** - adjust for new constructor signature
5. **Write mutation tests** - test `_mutate_weights`, `_mutate_new_node`, `_mutate_new_edge`
6. **Run black** on modified files
7. **Run all tests** to verify

## Test Cases for InnovationTracker

### `get_or_create_node_from_split` tests:
- First call with an edge creates new HiddenNodeGene with incremented ID
- Second call with same edge returns same node (same ID)
- Calls with different edges return different nodes with different IDs

### `get_or_create_edge` tests:
- First call with node pair creates new EdgeGene with incremented IDs
- Second call with same node pair returns edge with same id/innovation_id but can have different weight/enabled
- Calls with different node pairs return edges with different innovation IDs

## Test Cases for Mutations

### `_mutate_weights` tests:
- Weight perturbation stays within limits
- Weight reset gives value within limits
- Disabled genes can be re-enabled
- Enabled genes stay enabled (no spurious disabling)

### `_mutate_new_node` tests:
- Splitting edge creates new hidden node
- Splitting edge creates two new edges
- Original edge is disabled
- New edges have correct weights (1.0 for in-edge, original for out-edge)
- Same edge split twice in same generation returns same node

### `_mutate_new_edge` tests:
- New edge connects valid nodes (not output->anything, not anything->input)
- Same connection created twice returns same innovation number
- Edge has random weight within limits
