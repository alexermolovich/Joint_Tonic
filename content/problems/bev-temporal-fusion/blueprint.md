---
{
  "schema_version": 1,
  "problem_id": "bev-temporal-fusion",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Fuse Temporal BEV State",
  "summary": "Fuse already aligned BEV history with current features using a supplied scalar gate per cell.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "bevformer",
    "bev-temporal-fusion"
  ],
  "paper_ids": [
    "2022-bevformer"
  ],
  "paper_sections": [
    "Spatial cross-attention projection and temporal BEV alignment; gated fusion and health checks are original teaching substitutes"
  ],
  "track_ids": [
    "paper-2022-bevformer"
  ],
  "prerequisite_problem_ids": [
    "bev-ego-motion-warp"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.fuse_bev",
  "physical_contract": {
    "frames": [
      "Current ego-aligned BEV grid"
    ],
    "units": {
      "values": "dimensionless features"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "7dff0b1febafbe94884e865a18e85aba650a1e8506a5d293d96f7d4767d23a90"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2203.17270"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Fuse Temporal BEV State

Implement `fuse_bev(current: np.ndarray, history: np.ndarray, history_valid: np.ndarray, gate: np.ndarray, reset: bool) -> np.ndarray`.

Fuse already aligned BEV history with current features using a supplied scalar gate per cell.
`current` and `history` are float64 (H,W,D), 1<=H,W<=128,1<=D<=64. `history_valid` is bool (H,W), `gate` float64 (H,W) in [0,1], and reset is a built-in bool. Return float64 (H,W,D). At valid cells and reset=False use `(1-gate)*current+gate*history`; otherwise copy current exactly. All inputs including ignored history must be finite and valid. The history has already been warped into the current ego grid; feature channels are dimensionless. Reset marks a sequence boundary. This deterministic gated teaching substitute exposes temporal state rules; it is not BEVFormer's learned temporal self-attention.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. current=`[[[2,4]]]`, history=`[[[10,0]]]`, valid=`[[True]]`, gate=`[[0.25]]`, reset=False returns `[[[4,3]]]`.
2. With those same inputs and reset=True, output is `[[[2,4]]]`. An invalid history cell also returns current regardless of its gate.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Build the effective per-cell gate and blend feature vectors. Time and output storage O(HWD).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
