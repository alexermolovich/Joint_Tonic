---
{
  "schema_version": 1,
  "problem_id": "eureka-reward-component-diagnostics",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Aggregate Reward-Component Diagnostics",
  "summary": "A reward can be numerically valid yet be dominated by a constant or oversized component.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-eureka",
    "policy-components"
  ],
  "paper_ids": [
    "2023-eureka"
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
  "entrypoint": "solution.reward_diagnostics",
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
      "https://arxiv.org/abs/2310.12931"
    ],
    "paper_card": "research/papers/robot-learning-rl/2023-eureka.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Aggregate Reward-Component Diagnostics

## Contract

components real (B,T,C), task_scores real (B,T), valid Boolean (B,T); 1<=B<=64, 1<=T<=1024, 1<=C<=16, total elements<=1e6, magnitudes<=1e6 including masked entries. Components are already weighted dimensionless rewards; task scores are independent dimensionless progress metrics. Flatten valid (episode,time) observations with equal weight per observation. Return dict count Python int; mean, std, mean_abs, correlation float64(C,). std is population standard deviation, computed with centered scaling to retain tiny nonconstant variation; correlation is Pearson covariance/(population_std_component*population_std_score), NaN if either exact standard deviation is zero. With no valid rows all four vectors NaN. Do not weight episodes equally or infer causal reward quality from correlation.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
