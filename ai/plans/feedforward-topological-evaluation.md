# Plan: Replace Iterative Network Execution with Topological Forward Pass

## Goal
Replace the current O(N²) iterative matrix multiplication approach with a single O(nodes+edges) topological forward pass for feedforward networks.

## Files to Modify

### 1. `/home/nibudd/dev/pyNEAT/PhenotypeUtility.py` - REWRITE
**Remove:**
- `construct_weights_matrix()`
- `construct_input_vector()`
- `extract_output_vector()`
- `_get_number_of_nodes()`
- `_add_edge_weights()`
- `_add_input_memory()` (the weight-100 hack)

**Add:**
- `evaluate_feedforward(genotype, inputs, transfer_function)` - main entry point
- `_initialize_node_values(genotype, inputs)` - set inputs/bias/zeros
- `_build_incoming_edges_map(genotype)` - map node_id → incoming edges
- `_topological_sort(genotype)` - Kahn's algorithm
- `_extract_outputs(genotype, node_values)` - return output values as np.array

### 2. `/home/nibudd/dev/pyNEAT/NeuralNetworkRunner.py` - DELETE
No longer needed with single-pass approach.

### 3. `/home/nibudd/dev/pyNEAT/test/ut/PhenotypeUtility/` - UPDATE TESTS
Current tests are commented out. Will need new tests for:
- `evaluate_feedforward()` with simple genotype
- `_topological_sort()` ordering correctness
- `_initialize_node_values()` input/bias handling

### 4. `/home/nibudd/dev/pyNEAT/test/ut/NeuralNetworkRunner/` - DELETE
Remove test directory for deleted class.

## Implementation Steps

1. **Rewrite PhenotypeUtility.py** with new functions
2. **Delete NeuralNetworkRunner.py**
3. **Update imports** in any files that use these modules (check StandardConfig.py, XorConfiguration.py)
4. **Write tests** for new PhenotypeUtility functions
5. **Clean up** old test files
6. **Run tests** to verify

## API Change

**Before:**
```python
weights = construct_weights_matrix(genotype)
input_vec = construct_input_vector(genotype.node_genes, inputs)
runner = NeuralNetworkRunner(config.transfer_function)
result = runner.run(weights, input_vec)
outputs = extract_output_vector(genotype.node_genes, result)
```

**After:**
```python
outputs = evaluate_feedforward(genotype, inputs, config.transfer_function)
```
