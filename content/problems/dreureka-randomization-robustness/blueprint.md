---
{
  "schema_version": 1,
  "problem_id": "dreureka-randomization-robustness",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compare Robustness Across Randomization Settings",
  "summary": "A physics setting can appear stronger merely because it was tested on easier rollout seeds.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-dr-eureka",
    "policy-components"
  ],
  "paper_ids": [
    "2024-dr-eureka"
  ],
  "paper_sections": [
    "Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer."
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
  "entrypoint": "solution.randomization_robustness",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Reward contributions and independent progress/success metrics are dimensionless and already normalized."
    },
    "axes": "Batch, rollout, time and component axes are defined in the contract",
    "timestamp_assumptions": "Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit.",
    "batching": "Batch, rollout, time and component axes are defined in the contract"
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
    "authoring_notes": "Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.",
    "primary_urls": [
      "https://arxiv.org/abs/2406.01967"
    ],
    "paper_card": "research/papers/robot-learning-rl/2024-dr-eureka.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compare Robustness Across Randomization Settings

## Contract

success and valid Boolean (G,N), 1<=G<=128, 0<=N<=4096, <=1e6 entries. Rows are fixed physical parameter settings and columns are the same recorded rollout seeds. Parameter values/units are provided by the surrounding experiment; this function only compares dimensionless outcomes without changing physics. baseline_index built-in int [0,G), min_pairs built-in int [1,4096]. Return dict counts int64(G,), success_rate float64(G,) using all valid trials (NaN none), paired_counts int64(G,), paired_delta float64(G,) mean(success_g-success_baseline) over jointly valid same-seed trials (NaN none), comparable bool(G,) paired_count>=min_pairs; worst_index Python int lowest paired_delta among comparable rows with tie lowest index, or -1. Baseline compared with itself gives delta0 where observed. Pairing avoids confounding different seed subsets; no confidence interval or complete reward-aware prior construction is claimed.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
