# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
python -m pytest test/

# Run tests with verbose output
python -m pytest test/ -v

# Run a single test file
python -m pytest test/ut/GenotypeMutator/test_sync_ids_from_genotype.py

# Run tests with coverage
python -m pytest test/ --cov=.

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt
```

## Architecture

pyNEAT implements the NEAT (NeuroEvolution of Augmenting Topologies) algorithm - an evolutionary algorithm that evolves neural network topology and weights simultaneously.

### Core Flow

```
Genotype → PhenotypeUtility → Weights Matrix → NeuralNetworkRunner → Output
```

### Key Components

**Gene Representation:**
- `NodeGene.py` - Abstract base class with subclasses: InputNodeGene, OutputNodeGene, BiasNodeGene, HiddenNodeGene
- `EdgeGene.py` - Connections between nodes with innovation_id for tracking structural mutations
- `Genotype.py` - Container holding node_genes and edge_genes lists

**Evolution:**
- `GenotypeMutator.py` - Applies NEAT mutations (weight perturbation, add node, add edge). Tracks last_node_id, last_edge_id, and last_innovation_id for consistent genome management
- `StandardConfig.py` - Base configuration with mutation rates and abstract methods for problem-specific evaluation

**Network Execution:**
- `PhenotypeUtility.py` - Converts genotype to executable form (weights matrix, input/output vectors)
- `NeuralNetworkRunner.py` - Executes network with sigmoid transfer function until convergence

**Problem Configuration:**
- `XorConfiguration.py` - Example implementation for XOR problem with minimal starting topology (1 bias + 2 inputs + 1 output)

### Design Patterns

- **Strategy Pattern**: StandardConfig defines algorithm parameters; subclasses implement problem-specific evaluation
- **Deep Copy for Immutability**: GenotypeMutator copies genotypes before mutation
- **Template Method**: `mutate_genotype()` orchestrates individual `_mutate_*()` methods
