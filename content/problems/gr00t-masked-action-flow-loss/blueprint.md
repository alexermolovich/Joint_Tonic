---
{
  "schema_version": 1,
  "problem_id": "gr00t-masked-action-flow-loss",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute a Masked Action Flow-Matching Loss",
  "summary": "Compute a Masked Action Flow-Matching Loss.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2025-gr00t-n1",
    "policy-components"
  ],
  "paper_ids": [
    "2025-gr00t-n1"
  ],
  "paper_sections": [
    "Noise-to-data flow matching with an explicit support mask; this captures the GR00T action objective family, not DDPM noise prediction or the complete published training recipe."
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
  "entrypoint": "solution.masked_action_flow_loss",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates."
    },
    "axes": "Explicit batch, time, embodiment and channel axes defined in the contract",
    "timestamp_assumptions": "Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time.",
    "batching": "Explicit batch, time, embodiment and channel axes defined in the contract"
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
    "authoring_notes": "Noise-to-data flow matching with an explicit support mask; this captures the GR00T action objective family, not DDPM noise prediction or the complete published training recipe.",
    "primary_urls": [
      "https://arxiv.org/abs/2503.14734"
    ],
    "paper_card": "research/papers/vla-embodied/2025-gr00t-n1.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compute a Masked Action Flow-Matching Loss

## Contract

prediction,clean_actions,noise real(B,H,D),common1<=B<=32,1<=H<=64,1<=D<=32; valid bool(B,H,D), true for supported supervised action entries. Prediction is velocity of the explicit noise-to-data path X(t)=(1-t)*noise+t*clean_actions; target=clean_actions-noise. Return dict loss Pythonfloat mean squared error over ALL valid scalar entries across the batch, per_example float64(B,) per-row valid-element mean (0forzero support), gradient float64(B,H,D)=analytic d(global loss)/d(prediction), exact0masked. If no valid entries, loss/per_example/gradient all0. Masked numeric inputs still must be finite/bounded. No DDPM noise target, time sampling or gradient through targets.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Noise-to-data flow matching with an explicit support mask; this captures the GR00T action objective family, not DDPM noise prediction or the complete published training recipe.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.

## Source convention

[GR00T N1 v1, Section 2.1](https://arxiv.org/html/2503.14734v1#S2.SS1) prints the target noise-minus-action alongside a noise-to-data interpolation. This exercise explicitly chooses the derivative of its stated path, action-minus-noise. It therefore teaches a self-consistent flow objective and does not claim numeric compatibility with that printed target or with released weights.
