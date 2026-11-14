---
{
  "schema_version": 1,
  "problem_id": "rma-parameter-change-recovery",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Evaluate Policy Recovery After a Parameter Change",
  "summary": "Recovery requires a sustained window of measured good tracking after the environment changes.",
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
  "entrypoint": "solution.recovery_metrics",
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

# Evaluate Policy Recovery After a Parameter Change

## Contract

`times` is real `(T,)`, strictly increasing in `[0, 1_000_000]` seconds. `errors` is real `(B, T)`, nonnegative and at most 1,000,000; `valid` is Boolean `(B, T)`. Bounds are `1 <= B <= 128`, `1 <= T <= 4096`. `change_index` is a built-in Python int in `[0, T)`, `hold_samples` is a built-in Python int in `[1, T]`, and `tolerance` is a scalar in `[0, 1_000_000]`.

The change occurs at `times[change_index]`. Find the earliest window start at or after that index whose next `hold_samples` records all exist, are valid, and have errors at most the tolerance. Missing records break the run; never compress them away.

Return a dictionary with `recovered` (Boolean `(B,)`), `index` (int64 `(B,)`, first qualifying start or -1), `delay` (float64 `(B,)`, start timestamp minus change timestamp, NaN if no run), `post_change_mean` (float64 `(B,)`, mean of all valid errors from the change onward, NaN if absent), and `counts` (int64 `(B,)`, number of those valid errors).

Delay reports the start of the verified stable window, although its evidence finishes later. Errors are dimensionless normalized tracking losses. This original diagnostic does not prove dynamical stability or reproduce the paper's benchmark.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
