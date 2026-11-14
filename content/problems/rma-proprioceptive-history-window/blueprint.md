---
{
  "schema_version": 1,
  "problem_id": "rma-proprioceptive-history-window",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Window Proprioceptive History",
  "summary": "Adaptation history records what the robot observed and did before the current decision.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2021-rapid-motor-adaptation",
    "policy-components"
  ],
  "paper_ids": [
    "2021-rapid-motor-adaptation"
  ],
  "paper_sections": [
    "Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark."
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
  "entrypoint": "solution.window_history",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds."
    },
    "axes": "Batch/history/latent axes and timestamp shapes defined in the contract",
    "timestamp_assumptions": "Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion.",
    "batching": "Batch/history/latent axes and timestamp shapes defined in the contract"
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
    "authoring_notes": "Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.",
    "primary_urls": [
      "https://arxiv.org/abs/2107.04034"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2021-rapid-motor-adaptation.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Window Proprioceptive History

## Contract

`observations` is real `(N, O)`, `actions` is real `(N, A)`, `episode_ids` is integer `(N,)` and `query_indices` is integer `(Q,)`. Bounds are `1 <= N <= 4096`, `1 <= O, A <= 32`, `0 <= Q <= 128`. Episode IDs are nonnegative and nondecreasing; queries lie in `[0, N)`. `history_length` is a built-in Python int in `[1, 64]`. Numeric observation/action magnitudes are at most 100.

Records use a common fixed control period. Observations and commands are normalized dimensionless channels; each command is issued after its same-row observation. For query row t, take H previous candidate rows `[t-H, t)`, retaining only nonnegative rows in the query's episode. Left-pad missing rows with zeros. Never include the query row itself.

Return a dictionary with `history` (float64 `(Q, H, O+A)`, observation channels followed by action channels), `valid` (Boolean `(Q, H)`) and `source_indices` (int64 `(Q, H)`, original row indices or -1 for padding). Preserve query order. Do not interpolate or carry history across episode boundaries.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
