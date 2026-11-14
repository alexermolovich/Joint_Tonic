---
{
  "schema_version": 1,
  "problem_id": "openvla-training-quantile-action-bins",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Quantize Actions from Training-Set Quantiles",
  "summary": "Quantize Actions from Training-Set Quantiles.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2024-openvla",
    "policy-components"
  ],
  "paper_ids": [
    "2024-openvla"
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
  "entrypoint": "solution.quantize_training_actions",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Normalized actions and token features are dimensionless; physical calibration is supplied upstream."
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
      "https://arxiv.org/abs/2406.09246"
    ],
    "paper_card": "research/papers/vla-embodied/2024-openvla.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Quantize Actions from Training-Set Quantiles

## Contract

Training real(N,D),2<=N<=10000,1<=D<=32; actions real(M,D),0<=M<=10000; bins integer scalar2..256. Fit per-channel1st and99th percentiles using NumPy linear quantile interpolation on TRAINING only. Reject any upper<=lower. Uniform bins BETWEEN those bounds, not equal-probability quantile bins. Quantize actions with floor(bins*clip((a-lower)/(upper-lower),0,1)) clipped0..bins-1. Return lower/upper float64(D,), codes int64(M,D), decoded float64(M,D) at bin CENTERS lower+(code+.5)*(upper-lower)/bins. This explicit K-bin teaching codec does not bind IDs to the released OpenVLA tokenizer.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
