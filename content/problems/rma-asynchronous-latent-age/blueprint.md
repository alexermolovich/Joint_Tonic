---
{
  "schema_version": 1,
  "problem_id": "rma-asynchronous-latent-age",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Track the Age of an Asynchronous Adaptation Latent",
  "summary": "A newly completed adaptation job can still describe old observations.",
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
  "entrypoint": "solution.select_adaptation_latent",
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

# Track the Age of an Asynchronous Adaptation Latent

## Contract

`control_times` is real `(N,)`, `completion_times` and `observation_times` are real `(M,)`, and `latents` is real `(M, L)`. Bounds are `0 <= N, M <= 4096`, `1 <= L <= 32`. Times lie in `[0, 1_000_000]` seconds; latent magnitudes are at most 100. Completion times increase strictly, and each observation time is at most its completion time. Observation times may be unordered because jobs can complete out of order. Control queries may also be unordered. `max_observation_age` is a scalar in `[0, 100]` seconds.

For each control time, choose the last job completed at or before it. Use that job even if its observations are older than a previous job's observations. Return a dictionary with `indices` (int64 `(N,)`, selected job or -1), `observation_age` and `completion_age` (float64 `(N,)`, control time minus the respective timestamp, NaN if absent), `usable` (Boolean `(N,)`, a job exists and observation age is at most the limit), and `context` (float64 `(N, L)`, selected latent if usable, otherwise zero).

This explicitly selects by latest completion and gates by observation age. Do not fall back to an earlier job, select a future completion or claim a real-time scheduling guarantee.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
