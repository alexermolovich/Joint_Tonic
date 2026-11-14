---
{
  "schema_version": 1,
  "problem_id": "rma-privileged-latent-supervision",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Build Privileged Dynamics-Latent Supervision",
  "summary": "Privileged simulator factors provide supervision that is unavailable on the deployed robot.",
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
  "entrypoint": "solution.latent_supervision",
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

# Build Privileged Dynamics-Latent Supervision

## Contract

`extrinsics` is real `(B, E)`, `encoder_weight` is real `(E, L)`, `encoder_bias` is real `(L,)`, `predicted_latents` is real `(B, L)` and `valid` is Boolean `(B,)`. Bounds are `1 <= B <= 128`, `1 <= E, L <= 32`; numeric magnitudes are at most 100. Extrinsics are already normalized simulator-only factors; latent coordinates are dimensionless.

Define frozen teacher targets `z = tanh(extrinsics @ encoder_weight + encoder_bias)`. This one-layer encoder is a declared teaching surrogate for the learned environment encoder. Return a dictionary with `targets` (float64 `(B, L)`, z on valid rows and zero elsewhere), `per_state` (float64 `(B,)`, mean squared prediction error over L channels, NaN when invalid), `loss` (Python float, mean over valid state losses, or zero when none exist), and `prediction_gradient` (float64 `(B, L)`, twice the residual divided by valid-state count times L, zero on invalid rows).

Teacher targets and parameters remain fixed. Do not return teacher gradients, update an optimizer or claim this is the complete RMA encoder architecture.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
