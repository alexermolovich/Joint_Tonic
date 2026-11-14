---
{
  "schema_version": 1,
  "problem_id": "soft-value-bellman-target",
  "content_version": "1.0.0",
  "status": "reviewed",
  "title": "Compute an Entropy-Regularized Bellman Target",
  "summary": "One-step critic targets combine immediate reward with a value estimate of the next physical state.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2018-soft-actor-critic",
    "policy-components"
  ],
  "paper_ids": [
    "2018-soft-actor-critic",
    "2021-implicit-q-learning"
  ],
  "paper_sections": [
    "Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction."
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
  "entrypoint": "solution.soft_bellman_target",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless."
    },
    "axes": "Explicit batch/sample/channel axes defined in the contract",
    "timestamp_assumptions": "One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs.",
    "batching": "Explicit batch/sample/channel axes defined in the contract"
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
    "authoring_notes": "Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.",
    "primary_urls": [
      "https://arxiv.org/abs/1801.01290",
      "https://arxiv.org/abs/2110.06169"
    ],
    "paper_card": "research/papers/robot-learning-rl/2018-soft-actor-critic.md",
    "manifest": "research/IMPLEMENTATION_BACKLOG.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Compute an Entropy-Regularized Bellman Target

## Contract

rewards and next_values are real (B,T), 1<=B<=64, 1<=T<=1024; terminated and valid are Boolean arrays of the same shape. gamma is a scalar in [0,1]. Return a new float64(B,T) array: reward+gamma*(not terminated)*next_value at valid entries, exact0 otherwise. next_values is already a soft value for original SAC or an expectile value for IQL; do not subtract entropy again. A time-limit truncation has terminated=False and uses the final observation before reset. All invalid numeric entries raise even under a false mask. No gradients through targets are computed.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
