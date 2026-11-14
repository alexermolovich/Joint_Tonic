---
{
  "schema_version": 1,
  "problem_id": "nerf-pose-residual-diagnostics",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Detect Bad Poses with Reprojection and Render Residuals",
  "summary": "Compute separate per-view geometric and photometric residual summaries with explicit missing-data flags.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "nerf",
    "nerf-pose-residual-diagnostics"
  ],
  "paper_ids": [
    "2020-nerf"
  ],
  "paper_sections": [
    "Continuous scene representation and volume rendering: calibrated rays; original residual diagnostics"
  ],
  "track_ids": [
    "paper-2020-nerf"
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
  "entrypoint": "solution.pose_diagnostics",
  "physical_contract": {
    "frames": [
      "Per-camera image plane"
    ],
    "units": {
      "values": "pixels and linear RGB residuals"
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
    "evaluator_sha256": "a79d9f52ebe6d010e195b0c2107209f460bff42199f39b7dbf914886c910e1be"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2003.08934"
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

# Detect Bad Poses with Reprojection and Render Residuals

Implement `pose_diagnostics(pixel_residuals: np.ndarray, color_residuals: np.ndarray, valid: np.ndarray, pixel_limit: float, color_limit: float) -> dict`.

Compute separate per-view geometric and photometric residual summaries with explicit missing-data flags.
`pixel_residuals` is float64 (V,N,2) measured-minus-predicted image coordinates in pixels; `color_residuals` (V,N,3) is measured-minus-rendered linear RGB in [-1,1]. `valid` is bool (V,N), same validity for both. 1<=V<=32,0<=N<=4096. Limits are built-in int/float non-bool, finite, pixel_limit in [0,1e6], color_limit in [0,1]. Return dict with float64(V,) "pixel_rmse" = sqrt(mean over valid samples of squared 2D norm), "color_rmse" = sqrt(mean over valid samples AND RGB channels of squared entries), bool(V,) "observed", and bool(V,) "flagged". Missing views have both metrics 0, observed=False, flagged=False. Flag an observed view iff either metric strictly exceeds its limit. Validate even masked residual entries. This diagnoses suspicious views; residuals cannot establish that pose, rather than motion/lighting/calibration, caused the failure.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One valid sample with pixel residual `[3,4]`, RGB residual `[1,0,0]` gives pixel_rmse=5 pixels and color_rmse=1/√3. Limits (5,0.6) do not flag it; equality passes.
2. A view with no valid samples reports metrics 0 and observed=False, flagged=False, even at zero limits. Missing evidence is not perfect rendering.

## Source and scope

[Primary source](https://arxiv.org/abs/2003.08934). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute masked sums and valid counts per view; report two metrics and their independent threshold gate. O(VN) time and O(VN) temporary storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
