---
{
  "schema_version": 1,
  "problem_id": "aligned-trajectory-position-error",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Evaluate Trajectory Error After Alignment",
  "summary": "Align time-matched estimated and reference camera positions before reporting absolute position error.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "orb-slam-3"
  ],
  "paper_ids": [
    "2020-orb-slam-3"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2020-orb-slam-3"
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
  "entrypoint": "solution.align_trajectory",
  "physical_contract": {
    "frames": [
      "Explicit world, body, camera or dimensionless scaled-state frame in the contract"
    ],
    "units": {
      "values": "Meters, seconds, radians, pixels, or dimensionless normalized quantities as defined per argument"
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
    "evaluator_sha256": "ec591d64693e4b1e8996943cdb43027d8d07975e19e33c7eeb0536a7411bcac6"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2007.11898"
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

# Evaluate Trajectory Error After Alignment

Implement `align_trajectory(estimated, reference, fit_scale)`.

Align time-matched estimated and reference camera positions before reporting absolute position error.

`estimated (N,3)` and `reference (N,3)` are float64, `3<=N<=8192`, finite absolute coordinates <=1e6. Rows already refer to the same timestamps; interpolation is outside this function. Reference positions use world meters. Estimated positions use meters when `fit_scale=False`, or one consistent arbitrary monocular scale when True. `fit_scale` must be a built-in bool.

Center both clouds to X,Y. Require estimated variance `sum(X*X)/N>1e-9`. Form C=Y.T@X/N and SVD U,s,Vt; require second singular value >1e-9 to exclude degenerate paired alignment support. Set D=diag(1,1,sign(det(U@Vt))) and proper rotation R=U@D@Vt. Scale is sum(s*diag(D))/variance if fit_scale, otherwise exactly 1; require scale>1e-9. Translation t=mean(reference)-scale*R@mean(estimated).

Return fresh float64 `rotation (3,3)`, `translation (3,)`, Python float `scale`, float64 `aligned (N,3)=scale*estimated@R.T+t`, float64 `errors (N,)` Euclidean position errors in meters, and Python float `rmse=sqrt(mean(errors^2))`. No reflection, orientation error, timestamp pairing or outlier removal is allowed. Degenerate systems raise ValueError. Alignment removes global pose/scale gauge; it does not show that local drift is absent or reproduce a complete trajectory benchmark protocol.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Estimated tetrahedron points `[[0,0,0],[1,0,0],[0,1,0],[0,0,1]]` as float64, reference `2*Rz(90deg)*point+[1,2,3]`, fit_scale=True: recovered scale 2, rotation Rz(90deg), translation `[1,2,3]`, RMSE zero up to floating error.
2. Use the same reference but fit_scale=False: scale remains exactly 1. The best rigid alignment still has nonzero error because translation and rotation cannot absorb the factor-of-two scale difference.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.11898). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Center the paired clouds, solve the 3x3 orthogonal Procrustes system by SVD with determinant correction, optionally fit global scale, then compute Euclidean position errors. O(N) time/storage beyond the fixed-size decomposition.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
