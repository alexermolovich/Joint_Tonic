---
{
  "schema_version": 1,
  "problem_id": "nerf-hierarchical-depth-sampling",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Sample Hierarchical Depth Intervals",
  "type": "function",
  "difficulty": "medium",
  "paper_ids": [
    "2020-nerf"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2020-nerf"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.hierarchical_samples",
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
      "Ordered metric depth along each supplied normalized ray"
    ],
    "units": {
      "edges_output": "meters",
      "weights_quantiles": "dimensionless"
    },
    "axes": "B rays,S intervals,K quantiles",
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
    "evaluator_sha256": "e9e65c438ab5317553f8b95b103f040e9e4a7fd25ae5a7c51ff938de1707d2c7"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2003.08934"
    ],
    "implementation_urls": []
  }
}
---

# Sample Hierarchical Depth Intervals

Coarse rendering weights tell a fine sampler where useful mass lies along a ray. Inverse-CDF sampling converts supplied quantiles into depths. The small mass floor keeps every interval reachable without needing a random generator inside the task.

```python
def hierarchical_samples(edges, weights, quantiles):
    ...
```

## Function contract

Inputs: `edges: float64(B, S+1)`, `weights: float64(B, S)` and `quantiles: float64(B, K)`. Bounds: `1<=B<=32`, `1<=S, K<=128`. Depth edges are meters in `[0, 1000]`, strictly increasing with every gap at least `1e-9`. Weights are nonnegative and at most `1e6`; quantiles lie in `[0, 1]` and may be in arbitrary order.

Add `1e-5` to every weight, normalize masses per ray, and construct `CDF = [0, cumsum(probabilities)]`, setting the final entry exactly to 1. For each quantile use right-sided search, subtract one, and clip the interval index to `[0, S-1]`. Linearly interpolate from that CDF interval into its metric edge interval.

Return `float64(B, K)` depths preserving quantile order. Quantiles 0 and 1 return the near/far edges. Do not multiply masses by interval widths; supplied weights are masses, not densities. There is no random draw or field-network evaluation.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Edges `[[0, 1, 3]]`, weights `[[0, 0]]` and quantiles `[[0,.25,.5,.75, 1]]` produce depths `[[0,.5, 1, 2, 3]]`.

**Example 2.** A single interval with edges `[[2, 6]]`, weight `[[5]]` and quantiles `[[.75,.25]]` produces `[[5, 3]]`, preserving the unsorted query order.

## Source and scope

Original bounded component based on [2020-nerf](https://arxiv.org/abs/2003.08934). A neural scene model can spend more field queries near visible surfaces. Multiplying supplied masses by interval widths again biases the sampling distribution. This component does not evaluate a field, train NeRF or certify obstacle occupancy.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
