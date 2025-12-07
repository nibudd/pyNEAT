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
Genotype → PhenotypeUtility.evaluate_feedforward() → Output
```

Internally: topological sort → single forward pass through nodes

### Key Components

**Gene Representation:**
- `NodeGene.py` - Abstract base class with subclasses: InputNodeGene, OutputNodeGene, BiasNodeGene, HiddenNodeGene
- `EdgeGene.py` - Connections between nodes with innovation_id for tracking structural mutations
- `Genotype.py` - Container holding node_genes and edge_genes lists

**Evolution:**
- `GenotypeMutator.py` - Applies NEAT mutations (weight perturbation, add node, add edge). Tracks last_node_id, last_edge_id, and last_innovation_id for consistent genome management
- `StandardConfig.py` - Base configuration with mutation rates and abstract methods for problem-specific evaluation

**Network Execution:**
- `PhenotypeUtility.py` - Evaluates feedforward networks using topological sort and single forward pass

**Problem Configuration:**
- `XorConfiguration.py` - Example implementation for XOR problem with minimal starting topology (1 bias + 2 inputs + 1 output)

### Design Patterns

- **Strategy Pattern**: StandardConfig defines algorithm parameters; subclasses implement problem-specific evaluation
- **Deep Copy for Immutability**: GenotypeMutator copies genotypes before mutation
- **Template Method**: `mutate_genotype()` orchestrates individual `_mutate_*()` methods

## Project Conventions

- **Plans**: Store all implementation plans in `ai/plans/` with descriptive filenames
- **Reference Materials**: NEAT paper and reference implementations are in `ai/`

## Code Style

- **Test names**: Include both context and expected result (e.g., `test_network_with_no_edges_returns_sigmoid_of_zero`)
- **Docstrings**: Only include when they add important context beyond what the function name conveys
- always run black on a file after making changes to it