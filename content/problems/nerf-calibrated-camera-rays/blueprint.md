---
{
  "schema_version": 1,
  "problem_id": "nerf-calibrated-camera-rays",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Generate Calibrated Camera Rays",
  "summary": "Turn supplied continuous pixel coordinates into world-space unit rays.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "nerf",
    "nerf-calibrated-camera-rays"
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
  "prerequisite_problem_ids": [
    "project-camera-points"
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
  "entrypoint": "solution.camera_rays",
  "physical_contract": {
    "frames": [
      "Camera optical frame to caller-defined right-handed world"
    ],
    "units": {
      "values": "pixels and meters"
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
    "evaluator_sha256": "4461c1ec8d21e0e506d58bae6d8803e054e1ea3819f72f7c98c6999e563175ea"
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

# Generate Calibrated Camera Rays

Implement `camera_rays(pixels: np.ndarray, intrinsics: np.ndarray, camera_to_world: np.ndarray) -> tuple[np.ndarray, np.ndarray]`.

Turn supplied continuous pixel coordinates into world-space unit rays.
`pixels` is (N,2), 0<=N<=4096, ordered (u,v) in pixels; values may lie outside an image. `intrinsics` is (3,3), exactly [[fx,0,cx],[0,fy,cy],[0,0,1]], fx,fy>=1e-6. `camera_to_world` is (4,4): last row [0,0,0,1], rotation R satisfies R.T@R≈I and det(R)≈1 with absolute tolerance 1e-8, translation t in meters. Camera axes are x right,y down,z forward; world axes are caller-declared right-handed axes. Return origins (N,3), each t, and normalized world directions (N,3). Use d_c=[(u-cx)/fx,(v-cy)/fy,1]; rotate with R then normalize. No pixel-center offset is added: callers supply their chosen centers. No distortion, NDC conversion, scene normalization, or ray sampling occurs.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. With identity intrinsics/pose, pixels `[[0,0],[1,0]]` yield origins `[[0,0,0],[0,0,0]]`, directions `[[0,0,1],[1/√2,0,1/√2]]`.
2. With fx=fy=2,cx=cy=1, pixel `[[1,1]]` and identity rotation plus translation `[3,0,2]`, the ray starts `[3,0,2]` and points `[0,0,1]`. Translation changes origin, never direction.

## Source and scope

[Primary source](https://arxiv.org/abs/2003.08934). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Invert focal scaling analytically, rotate all directions, normalize each row, and copy the camera center for every origin. Time and storage O(N).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
