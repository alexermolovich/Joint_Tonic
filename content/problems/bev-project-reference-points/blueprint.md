---
{
  "schema_version": 1,
  "problem_id": "bev-project-reference-points",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Project BEV Reference Points into Calibrated Cameras",
  "summary": "Project ego-frame reference points into every camera without clipping image bounds.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "bevformer",
    "bev-project-reference-points"
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
    "se3-transform-points",
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
  "entrypoint": "solution.project_bev",
  "physical_contract": {
    "frames": [
      "Ego x-forward/y-left/z-up to optical x-right/y-down/z-forward"
    ],
    "units": {
      "values": "meters and pixels"
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
    "evaluator_sha256": "b01b389b74f7144aeb6e11d0195be28d8cd4c6c5a9a4cffc019f16a12765adca"
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

# Project BEV Reference Points into Calibrated Cameras

Implement `project_bev(points: np.ndarray, ego_to_camera: np.ndarray, intrinsics: np.ndarray) -> tuple[np.ndarray, np.ndarray]`.

Project ego-frame reference points into every camera without clipping image bounds.
`points` (N,3), 0<=N<=4096, meters in ego x-forward,y-left,z-up. `ego_to_camera` (C,4,4), 1<=C<=16, rigid transforms mapping ego to optical x-right,y-down,z-forward. Validate R.T@R≈I, det(R)≈1 at absolute tolerance 1e-8 and exact homogeneous last row. `intrinsics` (C,3,3), exact pinhole form [[fx,0,cx],[0,fy,cy],[0,0,1]], fx,fy>=1e-6. Return `(uv, depth)` float64 shapes (C,N,2),(C,N). Depth is camera z in meters. For z>1e-6 return u=fx*x/z+cx,v=fy*y/z+cy. For z<=1e-6 return exact [0,0] sentinel while retaining signed depth. Visibility is a separate problem; a [0,0] pixel is not itself invalid. Inputs are synchronized and undistorted.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. For one identity camera, K=I, points `[[2,4,2],[0,0,-1]]` give uv `[[[1,2],[0,0]]]` and depth `[[2,-1]]`.
2. Add a second camera translated +1 meter along optical x. Point `[0,0,2]` projects to `[0,0]` in camera 0 and `[0.5,0]` in camera 1; both depths are 2 meters.

## Source and scope

[Primary source](https://arxiv.org/abs/2203.17270). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Transform each point into each camera, project valid depths, and keep depth separate. Time and storage O(CN).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
