---
{
  "schema_version": 1,
  "problem_id": "pi0-solver-trajectory-error",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Evaluate Solver Steps Against Trajectory Error",
  "summary": "Evaluate Solver Steps Against Trajectory Error.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-pi0",
    "policy-components"
  ],
  "paper_ids": [
    "2024-pi0"
  ],
  "paper_sections": [
    "Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied."
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
  "entrypoint": "solution.solver_trajectory_error",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Actions are normalized dimensionless; error same units; measured solver latency and deadline milliseconds; flow step count dimensionless."
    },
    "axes": "Explicit batch, sequence and channel axes defined in the contract",
    "timestamp_assumptions": "Caller-synchronized observations; generation time and physical control time are distinct.",
    "batching": "Explicit batch, sequence and channel axes defined in the contract"
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
    "authoring_notes": "Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.",
    "primary_urls": [
      "https://arxiv.org/abs/2410.24164v4"
    ],
    "paper_card": "research/papers/vla-embodied/2024-pi0.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Evaluate Solver Steps Against Trajectory Error

## Contract

estimates real(K,H,D),1<=K<=64,1<=H<=256,1<=D<=32; target real(H,D), steps integer(K,) strictlypositive<=10000 (duplicates allowed), latency_ms real(K,) nonnegative. max_rmse/deadline_ms real scalars0..1e6. Each candidate is a FINAL action chunk from a supplied solver step count, not an intermediate flow state. Return rmse float64(K,) over H*D, max_abs_error float64(K,), feasible bool(K,) requiring RMSE<=max_rmse and latency<=deadline, selected_index Pythonint: among feasible candidates minimize latency, then steps, then originalindex; -1 if none. No model inference or claim that more steps always improves output.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
