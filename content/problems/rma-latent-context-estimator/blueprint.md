---
{
  "schema_version": 1,
  "problem_id": "rma-latent-context-estimator",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Estimate a Latent Dynamics Context",
  "summary": "A temporal adaptation module turns normalized sensor/action history into policy context.",
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
  "entrypoint": "solution.estimate_context",
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

# Estimate a Latent Dynamics Context

## Contract

`history` is real `(B, H, F)`, `valid` is Boolean `(B, H)`, `temporal_kernel` is real `(3, F, C)`, `weight` is real `(H*C, L)` and `bias` is real `(L,)`. Bounds are `1 <= B, H, F <= 32`, `1 <= C, L <= 16`; numeric magnitudes are at most 100. History is chronological normalized state/action data. Each mask row must be a suffix of true entries following optional false left padding; all-false is allowed.

Zero invalid history rows and pad one zero row at each temporal end. Compute width-three temporal cross-correlation without reversing the kernel: `conv[b,t,c] = sum(padded_history[b,t+k,f] * kernel[k,f,c])` over k and f. Apply ReLU, then zero every invalid temporal output. Flatten in chronological/channel order and apply the supplied linear weight and bias.

Return `latent` (float64 `(B, L)`) and `used` (Boolean `(B,)`, any valid history) in a dictionary. For an all-false history, return an exact zero latent rather than the bias. This original one-block adaptation surrogate is not the paper's full trained temporal network. It uses no privileged factors during inference.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
