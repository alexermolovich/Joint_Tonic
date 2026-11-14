---
{
  "schema_version": 1,
  "problem_id": "exposure-photometric-residual",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Compute an Exposure-Corrected Photometric Residual",
  "summary": "Compute exposure-corrected photometric residuals and a weighted Huber objective for aligned image samples.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "direct-sparse-odometry"
  ],
  "paper_ids": [
    "2016-direct-sparse-odometry"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2016-direct-sparse-odometry"
  ],
  "prerequisite_problem_ids": [
    "warp-calibrated-pixels"
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
  "entrypoint": "solution.photometric_residual",
  "physical_contract": {
    "frames": [
      "Right-handed camera, lidar, world or initial IMU frame as explicitly defined"
    ],
    "units": {
      "values": "Meters, radians, seconds, pixels and declared derivatives; intensity dimensionless"
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
    "evaluator_sha256": "8e4d6384d11de7b4a75a412be125b1a19893713607455f64b174cf854da15ddd"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1607.02565"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Compute an Exposure-Corrected Photometric Residual

Implement `photometric_residual(source, target, exposures, log_gains, offsets, weights, huber_delta)`.

Compute exposure-corrected photometric residuals and a weighted Huber objective for aligned image samples.

`source` and `target` are float64 `(N,)` intensities in `[0,1]`; `weights` is float64 `(N,)` in `[0,1]`; `0<=N<=65536`. `exposures` is float64 `(2,)` ordered source,target seconds in `[1e-6,1]`; `log_gains` is float64 `(2,)` in `[-10,10]`; `offsets` is float64 `(2,)` in `[-1,1]` intensity units. `huber_delta` is a Python int/float in `[1e-6,1]` intensity units. Samples are already geometrically aligned and photometrically calibrated; no image warp or parameter estimation is requested.

Let ratio=`(exposures[1]/exposures[0])*exp(log_gains[1]-log_gains[0])` and residual `r=(target-offsets[1])-ratio*(source-offsets[0])`. Use the half-quadratic Huber convention: `rho(r)=0.5*r*r` when `abs(r)<=delta`, otherwise `delta*(abs(r)-0.5*delta)`. Return a dictionary with fresh float64 `residual (N,)`, `energy (N,)=weights*rho(r)`, `target_gradient (N,)=weights*clip(r,-delta,delta)`, and Python float `total=sum(energy)`. The gradient holds all source/calibration parameters fixed. Zero samples give empty arrays and total zero. Output residual magnitude may exceed input bounds. The stated Huber normalization is this exercise's explicit convention.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Source `[0.2]`, target `[0.4]`, exposures `[0.01,0.02]`, zero log gains/offsets, weight `[1.]`, delta `0.1` yield residual `[0.]`, energy `[0.]`, target gradient `[0.]`, total `0`.
2. Source `[0.]`, target `[0.5]`, equal exposures, zero gains/offsets, weight `[0.5]`, delta `0.1` yield residual `[0.5]`, energy `[0.0225]`, target gradient `[0.05]`, total `0.0225`.

## Source and scope

[Primary source](https://arxiv.org/abs/1607.02565). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute the source-to-target brightness ratio, subtract the corrected source intensity, and evaluate the documented Huber value and target derivative. O(N) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
