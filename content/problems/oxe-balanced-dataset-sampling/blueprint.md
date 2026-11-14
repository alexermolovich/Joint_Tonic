---
{
  "schema_version": 1,
  "problem_id": "oxe-balanced-dataset-sampling",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Sample a Balanced Multi-Dataset Mixture",
  "summary": "Large datasets should not automatically dominate every mixed batch.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-open-x-embodiment",
    "policy-components"
  ],
  "paper_ids": [
    "2023-open-x-embodiment"
  ],
  "paper_sections": [
    "Original weighted mixture sampler motivated by OXE. Weights are explicit caller policy, not inferred from dataset size or asserted as the paper\u2019s exact proportions."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.sample_dataset_mixture",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Counts, weights and fractions are dimensionless; dataset action interfaces remain distinct."
    },
    "axes": "sizes/weights(G), uniforms(N,2) -> dataset/local indices(N)",
    "timestamp_assumptions": "Independent draws with replacement; selected local indices are not time coordinates.",
    "batching": "sizes/weights(G), uniforms(N,2) -> dataset/local indices(N)"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original weighted mixture sampler motivated by OXE. Weights are explicit caller policy, not inferred from dataset size or asserted as the paper\u2019s exact proportions.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.08864"
    ],
    "paper_card": "research/papers/vla-embodied/2023-open-x-embodiment.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Sample a Balanced Multi-Dataset Mixture

## Contract

`sample_dataset_mixture(sizes,weights,uniforms)` takes positive integer sizes(G,),1<=G<=128, sizes<=1e6; nonnegative real weights(G,) with positive sum; real uniforms(N,2),0<=N<=10000, entries[0,1). Normalize weights to probabilities and form cumulative sums in input dataset order. For each(u,v), choose the first dataset whose cumulative probability is strictly greater than u (searchsorted side=right); choose local index floor(v*sizes[g]). Zero-weight datasets must never be selected. Return (dataset_ids:int64(N,), local_indices:int64(N,)). Set final CDF entry to1 to avoid cumulative roundoff; no RNG calls.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original weighted mixture sampler motivated by OXE. Weights are explicit caller policy, not inferred from dataset size or asserted as the paper’s exact proportions.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.

Build the cumulative distribution over positive-weight datasets only, keeping their original indices; force its last value to exactly 1. This prevents floating-point roundoff from selecting a trailing zero-weight source.
