---
{
  "schema_version": 1,
  "problem_id": "bev-camera-health-diagnostics",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Diagnose Camera Dropout and Calibration Drift in BEV",
  "summary": "Distinguish missing camera frames from high reprojection residuals in a synchronized window.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "bevformer",
    "bev-camera-health-diagnostics"
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
  "prerequisite_problem_ids": [],
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
  "entrypoint": "solution.camera_health",
  "physical_contract": {
    "frames": [
      "Per-camera optical image coordinates"
    ],
    "units": {
      "values": "pixels and fraction of expected frames"
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
    "evaluator_sha256": "52b51669d01cded9ce32c196d2ff7c61c4ce62d13ed517699d0d7f7414a1a0f2"
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

# Diagnose Camera Dropout and Calibration Drift in BEV

Implement `camera_health(received: np.ndarray, residuals: np.ndarray, valid: np.ndarray, max_dropout: float, max_rmse: float) -> dict`.

Distinguish missing camera frames from high reprojection residuals in a synchronized window.
`received` is bool (C,T),1<=C<=16,1<=T<=4096; each False is one expected but missing frame. `residuals` float64 (C,T,2) contains one landmark displacement in pixels per frame; `valid` bool (C,T) marks usable landmark residuals and must imply received=True. Limits are built-in int/float non-bool: max_dropout in [0,1], max_rmse in [0,1e6]. Return dict arrays (C,): float64 "dropout_rate", "reprojection_rmse", bool "observed", "dropout_alert", "calibration_alert". Dropout is missing_count/T. RMSE is sqrt(mean squared 2D norm over valid residuals), zero if none; observed means any valid residual. Alerts use strict > thresholds; calibration_alert also requires observed. Validate all residuals even if masked. These are diagnostic flags, not proof of calibration drift or an automatic recalibration command.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. received=`[[True,False]]`, valid=`[[True,False]]`, residuals=`[[[3,4],[0,0]]]`, limits (0.25,4) report dropout 0.5, RMSE 5, both alerts True.
2. An entirely missing two-frame window has dropout 1, RMSE placeholder 0, observed=False, calibration_alert=False. It may trigger dropout_alert, but supplies no calibration evidence.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Reduce reception counts and residual sums per camera. O(CT) time and temporary storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
