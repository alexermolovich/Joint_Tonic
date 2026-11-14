---
{
  "schema_version": 1,
  "problem_id": "oxe-normalize-action-spaces",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Normalize and Mask Embodiment-Specific Action Spaces",
  "summary": "A shared model can reserve channels that some robots do not possess.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-open-x-embodiment",
    "policy-components"
  ],
  "paper_ids": [
    "2023-open-x-embodiment"
  ],
  "paper_sections": [
    "Original normalization/masking component inspired by OXE cross-embodiment learning. Missing dimensions are masked, not treated as observed zero commands."
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
  "entrypoint": "solution.normalize_action_spaces",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Each action channel retains its declared controller unit in inputs; per-channel mean/std use that unit, output is dimensionless."
    },
    "axes": "actions(B,H,D), available/mean/std(B,D) -> normalized/mask(B,H,D)",
    "timestamp_assumptions": "H is an equally spaced action horizon supplied by the dataset; normalization does not change timing or controller frames.",
    "batching": "actions(B,H,D), available/mean/std(B,D) -> normalized/mask(B,H,D)"
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
    "authoring_notes": "Original normalization/masking component inspired by OXE cross-embodiment learning. Missing dimensions are masked, not treated as observed zero commands.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.08864"
    ],
    "paper_card": "research/papers/vla-embodied/2023-open-x-embodiment.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Normalize and Mask Embodiment-Specific Action Spaces

## Contract

`normalize_action_spaces(actions,available,mean,std)` receives real actions(B,H,D),1<=B<=32,1<=H<=256,1<=D<=64; available:bool(B,D); mean,std:real(B,D), std>=1e-6. Return (normalized:float64(B,H,D), mask:bool(B,H,D)), with normalized=(actions-mean)/std where available and exact0 otherwise; mask broadcasts available across horizon using fresh storage. Validate all entries including unavailable channels. Inputs already share channel ordering; no clipping or action padding is inferred.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original normalization/masking component inspired by OXE cross-embodiment learning. Missing dimensions are masked, not treated as observed zero commands.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
