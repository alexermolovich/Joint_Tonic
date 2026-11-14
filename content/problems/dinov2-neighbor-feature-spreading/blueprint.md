---
{
  "schema_version": 1,
  "problem_id": "dinov2-neighbor-feature-spreading",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Implement Nearest-Neighbor Feature-Spreading Regularization",
  "type": "function",
  "difficulty": "medium",
  "paper_ids": [
    "2023-dinov2"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2023-dinov2"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.neighbor_spreading",
  "owners": [
    "root"
  ],
  "reviewers": [
    "research_curator"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "physical_contract": {
    "frames": [
      "Encoder feature coordinates; no physical frame transform"
    ],
    "units": {
      "features_distances_loss": "dimensionless"
    },
    "axes": "N feature rows,D channels; neighbor indices refer to original rows",
    "timestamp_assumptions": "Fixed supplied batch; cameras/observations are aligned by caller. No clock inference, state history or real-time guarantee.",
    "batching": "Only explicitly declared dimensions; masks preserve original ordering."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-mechanism-oracle",
      "boundary-and-invalid-input",
      "maximum-advertised-dimensions",
      "input-preservation-and-output-aliasing"
    ],
    "performance_class": "none",
    "evaluator_sha256": "d57b30628eefb900b42b4806c56a3adee7f7651a812ea44af321138070b614ee"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.07193"
    ],
    "implementation_urls": []
  }
}
---

# Implement Nearest-Neighbor Feature-Spreading Regularization

A representation can collapse when many images receive nearly identical features. A nearest-neighbor spreading penalty discourages crowding on the unit sphere. It is possible for this loss to be negative: distances greater than one have positive logarithms.

```python
def neighbor_spreading(features, epsilon):
    ...
```

## Function contract

Input `features` is `float64(N, D)`, with `2<=N<=128`, `1<=D<=64` and each row's L2 norm at least `1e-9`. Python real `epsilon` lies in `[1e-8, 0.1]`.

Normalize each row to unit L2 norm. For each row, find its closest OTHER row in Euclidean distance, choosing the smallest original row index on ties. Return `distances: float64(N,)`, `neighbors: int64(N,)` and `loss: Python float`, equal to `-mean(log(max(distance, epsilon)))`.

Distances are returned unclamped; epsilon affects only the logarithm. Duplicate features are allowed and have distance zero. This is an explicitly clamped KoLeo-style teaching convention, not a claim to match every numerical detail of the released implementation. No gradients or encoder training are requested.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Features `[[1, 0],[-1, 0]]` with epsilon `.01` return distances `[2, 2]`, neighbors `[1, 0]`, and loss `-log(2)`.

**Example 2.** Three identical nonzero feature rows return distances `[0, 0, 0]`, neighbors `[1, 0, 0]`, and loss `-log(epsilon)`. The diagonal is excluded even when other rows are duplicates.

## Source and scope

Original bounded component based on [2023-dinov2](https://arxiv.org/abs/2304.07193). Reusable visual features should distinguish different scenes before a robot policy consumes them. Accidentally selecting each feature as its own neighbor makes every distance zero and destroys the intended learning signal.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
