# pyNEAT Implementation Status

Reference materials:
- `NEAT-paper.pdf` - Original Stanley & Miikkulainen (2002) paper
- `marIO.lua` - SethBling's working NEAT implementation for Super Mario

---

## Completed Tasks

### Gene Representation
- [x] `NodeGene.py` - Abstract base class with subclasses (InputNodeGene, OutputNodeGene, BiasNodeGene, HiddenNodeGene)
- [x] `NodeType.py` - Enum for node classification
- [x] `EdgeGene.py` - Connection genes with `id`, `innovation_id`, `in_node`, `out_node`, `weight`, `enabled`
- [x] `Genotype.py` - Container holding `node_genes` and `edge_genes` lists

### Mutation Operations
- [x] `GenotypeMutator.py` - Implements:
  - [x] Weight mutation (perturb or reset)
  - [x] Add node mutation (split existing connection)
  - [x] Add edge mutation (connect two unconnected nodes)
  - [x] ID tracking (`last_node_id`, `last_edge_id`, `last_innovation_id`)

### Network Execution
- [x] `PhenotypeUtility.py` - Evaluates feedforward networks:
  - [x] `evaluate_feedforward()` - Single forward pass using topological sort
  - [x] `_topological_sort()` - Kahn's algorithm for node ordering
  - [x] `_initialize_node_values()` - Set inputs/bias/zeros
  - [x] `_build_incoming_edges_map()` - Map nodes to incoming edges
  - [x] `_extract_outputs()` - Return output values

### Configuration
- [x] `StandardConfig.py` - Base configuration with mutation rates, abstract methods
- [x] `XorConfiguration.py` - XOR problem implementation

---

## Incomplete Tasks

### 1. Add Missing Tests

**Purpose**: Ensure existing code is properly tested before building new features on top of it.

**Current test status**:

| Source File | Test File | Status |
|-------------|-----------|--------|
| `GenotypeMutator.py` | `test_sync_ids_from_genotype.py` | **8 active tests** - only covers `_sync_ids_from_genotype()` |
| `PhenotypeUtility.py` | `test_evaluate_feedforward.py` | **10 active tests** - covers `evaluate_feedforward()` |
| `EdgeGene.py` | None | No tests |
| `NodeGene.py` | None | No tests |
| `Genotype.py` | None | No tests |

**Implementation outline**:

#### High Priority (Critical Logic)

1. **Add GenotypeMutator mutation tests** (`test/ut/GenotypeMutator/`)
   - `_mutate_weights()` - test weight perturbation and reset
   - `_mutate_new_node()` - test edge splitting, new node creation
   - `_mutate_new_edge()` - test new connection creation
   - `mutate_genotype()` - test full mutation pipeline
   - Test probability checks: `_weight_is_mutating()`, `_edge_is_splitting()`, etc.

#### Medium Priority (Data Classes)

2. **Add NodeGene tests** (`test/ut/NodeGene/`)
   - Test `is_input()`, `is_output()`, `is_bias()` return correct values for each subclass
   - Test that base `NodeGene` returns `False` for all type checks

3. **Add Genotype tests** (`test/ut/Genotype/`)
   - Test `describe()` method output formatting

#### Low Priority

4. **EdgeGene tests** - Simple data container, optional
5. **Config tests** - Configuration values, optional

**Files to create**:
- `test/ut/GenotypeMutator/test_mutate_weights.py`
- `test/ut/GenotypeMutator/test_mutate_new_node.py`
- `test/ut/GenotypeMutator/test_mutate_new_edge.py`
- `test/ut/NodeGene/test_node_gene.py` (optional)
- `test/ut/Genotype/test_genotype.py` (optional)

---

### 2. Crossover

**Purpose**: Combine two parent genomes into offspring by aligning genes using innovation numbers.

**Context from paper (Section 3.2)**:
- Genes with same `innovation_id` are "matching genes"
- Genes in one parent but not the other are "disjoint" (within range) or "excess" (beyond range)
- Matching genes: randomly inherit from either parent
- Disjoint/excess genes: inherit from the MORE FIT parent

**Context from marIO.lua** (lines 369-402):
```lua
function crossover(g1, g2)
    -- Make sure g1 is the higher fitness genome
    if g2.fitness > g1.fitness then
        tempg = g1; g1 = g2; g2 = tempg
    end

    local child = newGenome()

    -- Build lookup of g2's genes by innovation number
    local innovations2 = {}
    for i=1,#g2.genes do
        innovations2[g2.genes[i].innovation] = g2.genes[i]
    end

    -- Iterate through fitter parent's genes
    for i=1,#g1.genes do
        local gene1 = g1.genes[i]
        local gene2 = innovations2[gene1.innovation]
        if gene2 ~= nil and math.random(2) == 1 and gene2.enabled then
            table.insert(child.genes, copyGene(gene2))
        else
            table.insert(child.genes, copyGene(gene1))
        end
    end

    child.maxneuron = math.max(g1.maxneuron, g2.maxneuron)
    return child
end
```

**Implementation outline**:
1. Create `crossover(genotype1, genotype2, fitness1, fitness2)` function (in GenotypeMutator or new file)
2. Ensure higher-fitness parent is "primary"
3. Build a dict mapping `innovation_id` -> `EdgeGene` for secondary parent
4. For each edge in primary parent:
   - If matching gene exists in secondary and coin flip: use secondary's gene
   - Otherwise: use primary's gene
5. Copy all node genes needed (union of both parents' nodes, or derive from edges)
6. Handle disabled genes: 75% chance to stay disabled if disabled in either parent
7. Return new Genotype

**Files to modify**: `GenotypeMutator.py` or create new `Crossover.py`

---

### 2. Compatibility Distance

**Purpose**: Measure how "different" two genomes are to decide if they belong in the same species.

**Context from paper (Section 3.3, Equation 1)**:
```
δ = (c1 * E) / N + (c2 * D) / N + c3 * W̄

Where:
- E = number of excess genes
- D = number of disjoint genes
- W̄ = average weight difference of matching genes
- N = number of genes in larger genome (can be 1 if both < 20 genes)
- c1, c2, c3 = coefficients (paper uses c1=1.0, c2=1.0, c3=0.4)
```

**Context from marIO.lua** (lines 589-646):
```lua
function disjoint(genes1, genes2)
    -- Count genes in each that aren't in the other
    local i1 = {}
    for i = 1,#genes1 do i1[genes1[i].innovation] = true end
    local i2 = {}
    for i = 1,#genes2 do i2[genes2[i].innovation] = true end

    local disjointGenes = 0
    for i = 1,#genes1 do
        if not i2[genes1[i].innovation] then disjointGenes = disjointGenes+1 end
    end
    for i = 1,#genes2 do
        if not i1[genes2[i].innovation] then disjointGenes = disjointGenes+1 end
    end

    return disjointGenes / math.max(#genes1, #genes2)
end

function weights(genes1, genes2)
    -- Average weight difference of matching genes
    local i2 = {}
    for i = 1,#genes2 do i2[genes2[i].innovation] = genes2[i] end

    local sum = 0
    local coincident = 0
    for i = 1,#genes1 do
        if i2[genes1[i].innovation] ~= nil then
            sum = sum + math.abs(genes1[i].weight - i2[genes1[i].innovation].weight)
            coincident = coincident + 1
        end
    end
    return sum / coincident
end

function sameSpecies(genome1, genome2)
    local dd = DeltaDisjoint * disjoint(genome1.genes, genome2.genes)
    local dw = DeltaWeights * weights(genome1.genes, genome2.genes)
    return dd + dw < DeltaThreshold
end
```

**Implementation outline**:
1. Create `Species.py` or add to `StandardConfig.py`
2. Implement `count_disjoint_excess(genotype1, genotype2)` -> (disjoint, excess)
3. Implement `average_weight_difference(genotype1, genotype2)` -> float
4. Implement `compatibility_distance(genotype1, genotype2, c1, c2, c3)` -> float
5. Implement `is_same_species(genotype1, genotype2, threshold)` -> bool

**Files to create**: `Species.py` or `CompatibilityDistance.py`

---

### 4. Species Management

**Purpose**: Group genomes into species, track species over generations, handle stale species.

**Context from paper (Section 3.3)**:
- Each species is represented by a random genome from previous generation
- New genomes placed in first compatible species, or new species created
- Species that don't improve for 15 generations are removed (stagnation)

**Context from marIO.lua**:
```lua
function newSpecies()
    local species = {}
    species.topFitness = 0
    species.staleness = 0
    species.genomes = {}
    species.averageFitness = 0
    return species
end

function addToSpecies(child)
    local foundSpecies = false
    for s=1,#pool.species do
        local species = pool.species[s]
        if not foundSpecies and sameSpecies(child, species.genomes[1]) then
            table.insert(species.genomes, child)
            foundSpecies = true
        end
    end
    if not foundSpecies then
        local childSpecies = newSpecies()
        table.insert(childSpecies.genomes, child)
        table.insert(pool.species, childSpecies)
    end
end

function removeStaleSpecies()
    local survived = {}
    for s = 1,#pool.species do
        local species = pool.species[s]
        -- Sort by fitness descending
        table.sort(species.genomes, function(a,b) return a.fitness > b.fitness end)

        if species.genomes[1].fitness > species.topFitness then
            species.topFitness = species.genomes[1].fitness
            species.staleness = 0
        else
            species.staleness = species.staleness + 1
        end

        -- Keep if not stale OR if it's the best species overall
        if species.staleness < StaleSpecies or species.topFitness >= pool.maxFitness then
            table.insert(survived, species)
        end
    end
    pool.species = survived
end
```

**Implementation outline**:
1. Create `Species` class:
   - `genomes: List[Genotype]`
   - `representative: Genotype` (for compatibility comparison)
   - `top_fitness: float`
   - `staleness: int`
   - `average_fitness: float`
2. Implement `add_to_species(genome, species_list, threshold)`
3. Implement `remove_stale_species(species_list, stale_threshold, global_max_fitness)`
4. Implement `update_species_fitness(species)` - calculate average, update staleness

**Files to create**: `Species.py`

---

### 5. Fitness Sharing (Adjusted Fitness)

**Purpose**: Prevent any single species from dominating by dividing fitness among species members.

**Context from paper (Section 3.3, Equation 2)**:
```
f'_i = f_i / Σ sh(δ(i,j))

Where sh(δ) = 0 if δ > threshold, else 1
This simplifies to: adjusted_fitness = raw_fitness / species_size
```

**Context from marIO.lua** (lines 666-685):
```lua
function rankGlobally()
    local global = {}
    for s = 1,#pool.species do
        for g = 1,#pool.species[s].genomes do
            table.insert(global, pool.species[s].genomes[g])
        end
    end
    table.sort(global, function(a,b) return a.fitness < b.fitness end)
    for g=1,#global do
        global[g].globalRank = g
    end
end

function calculateAverageFitness(species)
    local total = 0
    for g=1,#species.genomes do
        total = total + species.genomes[g].globalRank
    end
    species.averageFitness = total / #species.genomes
end
```

Note: MarIO uses global rank instead of raw fitness for stability.

**Implementation outline**:
1. Add `adjusted_fitness` field to Genotype or track separately
2. Implement `calculate_adjusted_fitness(genome, species_size)` -> fitness / species_size
3. Implement `rank_globally(all_genomes)` - assign global rank by fitness
4. Implement `calculate_species_average_fitness(species)` using ranks or adjusted fitness

**Files to modify**: `Genotype.py`, `Species.py`

---

### 6. Selection and Reproduction

**Purpose**: Select parents for next generation, breed offspring proportional to species fitness.

**Context from paper**:
- Each species gets offspring proportional to sum of adjusted fitnesses
- Bottom performers in each species are eliminated before reproduction
- Champion of species with >5 members is copied unchanged (elitism)

**Context from marIO.lua** (lines 687-810):
```lua
function cullSpecies(cutToOne)
    for s = 1,#pool.species do
        local species = pool.species[s]
        table.sort(species.genomes, function(a,b) return a.fitness > b.fitness end)
        local remaining = math.ceil(#species.genomes/2)
        if cutToOne then remaining = 1 end
        while #species.genomes > remaining do
            table.remove(species.genomes)
        end
    end
end

function removeWeakSpecies()
    local survived = {}
    local sum = totalAverageFitness()
    for s = 1,#pool.species do
        local species = pool.species[s]
        local breed = math.floor(species.averageFitness / sum * Population)
        if breed >= 1 then
            table.insert(survived, species)
        end
    end
    pool.species = survived
end

function breedChild(species)
    local child = {}
    if math.random() < CrossoverChance then
        g1 = species.genomes[math.random(1, #species.genomes)]
        g2 = species.genomes[math.random(1, #species.genomes)]
        child = crossover(g1, g2)
    else
        g = species.genomes[math.random(1, #species.genomes)]
        child = copyGenome(g)
    end
    mutate(child)
    return child
end

function newGeneration()
    cullSpecies(false)           -- Remove bottom half
    rankGlobally()
    removeStaleSpecies()
    rankGlobally()
    for s = 1,#pool.species do
        calculateAverageFitness(pool.species[s])
    end
    removeWeakSpecies()

    local sum = totalAverageFitness()
    local children = {}
    for s = 1,#pool.species do
        local species = pool.species[s]
        local breed = math.floor(species.averageFitness / sum * Population) - 1
        for i=1,breed do
            table.insert(children, breedChild(species))
        end
    end

    cullSpecies(true)            -- Keep only champion

    -- Fill remaining slots
    while #children + #pool.species < Population do
        local species = pool.species[math.random(1, #pool.species)]
        table.insert(children, breedChild(species))
    end

    for c=1,#children do
        addToSpecies(children[c])
    end

    pool.generation = pool.generation + 1
end
```

**Implementation outline**:
1. Implement `cull_species(species, keep_ratio=0.5)` - remove bottom performers
2. Implement `remove_weak_species(species_list, population_size)` - remove species that can't breed
3. Implement `breed_child(species, crossover_chance, mutator)` - crossover or clone + mutate
4. Implement `calculate_offspring_count(species, total_avg_fitness, population_size)`
5. Implement `create_next_generation(species_list, population_size, config)`

**Files to create**: `Reproduction.py` or `Population.py`

---

### 7. Population / Pool Management

**Purpose**: Top-level container managing all species, generation count, and global innovation counter.

**Context from marIO.lua** (lines 201-212):
```lua
function newPool()
    local pool = {}
    pool.species = {}
    pool.generation = 0
    pool.innovation = Outputs  -- Start after output node innovations
    pool.currentSpecies = 1
    pool.currentGenome = 1
    pool.currentFrame = 0
    pool.maxFitness = 0
    return pool
end
```

**Implementation outline**:
1. Create `Population` class:
   - `species: List[Species]`
   - `generation: int`
   - `innovation_counter: int`
   - `max_fitness: float`
2. Implement `initialize_population(config, size)` - create minimal genomes
3. Implement `evaluate_population(fitness_function)` - run fitness on all genomes
4. Implement `evolve_generation()` - orchestrate selection, reproduction, speciation

**Files to create**: `Population.py`

---

### 8. Main Evolution Loop

**Purpose**: Orchestrate the complete NEAT algorithm from initialization to solution.

**Current state**: `main.py` contains pseudocode skeleton only.

**Implementation outline**:
1. Initialize population with minimal topology (no hidden nodes)
2. Loop until solution found or max generations:
   ```
   a. Evaluate fitness of all genomes
   b. Check for solution
   c. Update species fitness stats
   d. Remove stale species
   e. Calculate adjusted fitness / global ranks
   f. Remove weak species
   g. Breed next generation (crossover + mutation)
   h. Assign offspring to species
   i. Increment generation
   ```
3. Return best genome

**Files to modify**: `main.py`

---

## Suggested Implementation Order

1. **Add Missing Tests** - Ensure existing code works before building on it
2. **Compatibility Distance** - Foundation for speciation
3. **Species Management** - Group genomes, track staleness
4. **Fitness Sharing** - Adjusted fitness calculation
5. **Crossover** - Combine parent genomes
6. **Selection and Reproduction** - Breed next generation
7. **Population Management** - Top-level orchestration
8. **Main Evolution Loop** - Put it all together

---

## Key Parameters (from paper and marIO)

| Parameter | Paper Value | MarIO Value | Description |
|-----------|-------------|-------------|-------------|
| Population | 150-1000 | 300 | Number of genomes |
| c1 (excess coeff) | 1.0 | 2.0 | Compatibility distance |
| c2 (disjoint coeff) | 1.0 | (combined with c1) | Compatibility distance |
| c3 (weight coeff) | 0.4-3.0 | 0.4 | Compatibility distance |
| δt (threshold) | 3.0-4.0 | 1.0 | Species threshold |
| Stale generations | 15 | 15 | Before species removed |
| Crossover chance | 75% | 75% | vs mutation only |
| Weight mutation | 80% | 25% | Chance per genome |
| Perturb chance | 90% | 90% | vs reset weight |
| Add node chance | 3% | 50% | Structural mutation |
| Add link chance | 5-30% | 200% | Structural mutation |
| Disable inherit | 75% | - | If disabled in either parent |

Note: MarIO uses higher structural mutation rates, possibly because Mario requires more complex networks.

---

## Low Priority Tasks

### 9. Simplify StandardConfig

**Purpose**: Clean up the configuration class structure and naming.

**Current issues**:
- Name `StandardConfig` is unclear - consider `NeatConfig` or `Config`
- Mix of class attributes and abstract methods
- Some parameters may be unused or redundant

**Implementation outline**:
1. Rename `StandardConfig` to `NeatConfig` or similar
2. Review and remove unused parameters
3. Consider using dataclasses or attrs for cleaner structure
4. Update all references in dependent files

**Files to modify**: `StandardConfig.py`, `XorConfiguration.py`, `main.py`, tests

---

### 10. Set Up Linting with Pre-commit Hooks

**Purpose**: Automatically format and lint code on every change.

**Implementation outline**:
1. Add `ruff` or `flake8` to `requirements-dev.txt` for linting
2. Configure linting rules in `pyproject.toml`
3. Add `pre-commit` to `requirements-dev.txt`
4. Create `.pre-commit-config.yaml` with:
   - black (formatting)
   - ruff or flake8 (linting)
   - Optional: mypy (type checking)
5. Run `pre-commit install` to set up hooks
6. Fix any existing linting errors

**Files to create**: `.pre-commit-config.yaml`
**Files to modify**: `requirements-dev.txt`, `pyproject.toml`
