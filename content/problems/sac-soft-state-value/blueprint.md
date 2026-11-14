---
{
  "schema_version": 1,
  "problem_id": "sac-soft-state-value",
  "content_version": "1.0.0",
  "status": "reviewed",
  "title": "Compute an Entropy-Regularized State Value",
  "summary": "A stochastic robot policy values both task reward and action entropy.",
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
    "2018-soft-actor-critic"
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
  "entrypoint": "solution.soft_state_value",
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
      "https://arxiv.org/abs/1801.01290"
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

# Compute an Entropy-Regularized State Value

## Contract

q_values and log_probabilities are real (B,K), 1<=B<=128, 1<=K<=256; valid is Boolean of the same shape. Log densities lie in [-100,100], including positive continuous densities. alpha is a scalar in [0,100]. Return a dict values:float64(B,), counts:int64(B,). Each value is the valid sample mean of Q-alpha*log_probability in that row; a row with no valid action samples returns value0/count0. Do not softmax over Q or add probability weights: the supplied samples already follow the policy.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
