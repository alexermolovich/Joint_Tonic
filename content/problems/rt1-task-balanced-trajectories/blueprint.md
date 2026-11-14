---
{
  "schema_version": 1,
  "problem_id": "rt1-task-balanced-trajectories",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Sample a Task-Balanced Trajectory Batch",
  "summary": "A common task can dominate training when sampling trajectories uniformly.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2022-rt-1",
    "policy-components"
  ],
  "paper_ids": [
    "2022-rt-1"
  ],
  "paper_sections": [
    "Original task-balanced sampler motivated by multi-task RT-1 data; the exact two-stage inverse-CDF contract is a teaching choice, not a reproduction of its dataset distribution."
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
  "entrypoint": "solution.sample_task_balanced",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "IDs and sampling fractions are dimensionless; trajectory indices preserve the caller dataset ordering."
    },
    "axes": "task_ids(M), uniforms(N,2) -> trajectory_indices(N)",
    "timestamp_assumptions": "One row is one independent draw with replacement, not a control timestep.",
    "batching": "task_ids(M), uniforms(N,2) -> trajectory_indices(N)"
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
    "authoring_notes": "Original task-balanced sampler motivated by multi-task RT-1 data; the exact two-stage inverse-CDF contract is a teaching choice, not a reproduction of its dataset distribution.",
    "primary_urls": [
      "https://arxiv.org/abs/2212.06817"
    ],
    "paper_card": "research/papers/vla-embodied/2022-rt-1.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Sample a Task-Balanced Trajectory Batch

## Contract

`sample_task_balanced(task_ids, uniforms)` receives integer task_ids(M,), 1<=M<=10000, nonnegative IDs<=1e6, and real uniforms(N,2), 0<=N<=10000, with entries in [0,1). Sort unique task IDs increasingly. For each row (u,v), choose sorted task index floor(u*G), then choose floor(v*count) within that task’s original trajectory indices. Return int64 indices(N,). Empty uniforms shape(0,2) returns empty; task_ids cannot be empty. No RNG call is made.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original task-balanced sampler motivated by multi-task RT-1 data; the exact two-stage inverse-CDF contract is a teaching choice, not a reproduction of its dataset distribution.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
