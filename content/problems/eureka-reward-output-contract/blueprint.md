---
{
  "schema_version": 1,
  "problem_id": "eureka-reward-output-contract",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Validate a Reward Function Contract",
  "summary": "A reward callback needs a measurable interface before it can guide learning.",
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
  "entrypoint": "solution.validate_reward_output",
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

# Validate a Reward Function Contract

## Contract

rewards real array-like (B,), components real (B,C), valid Boolean (B,), 0<=B<=4096, 1<=C<=32. Unlike ordinary finite numeric inputs, rewards/components may contain NaN/Inf: these are evidence to diagnose, not an exception. Require floating or integer real dtype (not bool/object/complex); all finite magnitudes <=1e6. reward_bound finite scalar [0,1e6], atol [0,1]. Components are already weighted dimensionless contributions, expected to sum to reward. Return dict finite bool(B): reward and all components finite; bounded bool(B): finite AND abs(reward)<=bound AND every abs(component)<=bound; consistent bool(B): finite AND abs(reward-sum(components))<=atol; accepted bool(B): valid AND finite AND bounded AND consistent; all_valid_accepted Python bool all accepted on valid rows (vacuously True with no valid rows); invalid_count Python int number of valid rejected rows. Diagnose even invalid-mask rows but exclude them from acceptance and aggregate count. No executable code is accepted; this checks captured reward-function outputs, not semantic task alignment.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, follow the stated nonfinite-evidence exception, with finite absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
