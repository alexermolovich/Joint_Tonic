---
{
  "schema_version": 1,
  "problem_id": "reprojection-pose-hypothesis-inliers",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Select Geometric Pose Inliers",
  "summary": "Compare supplied camera-pose hypotheses using normalized geometric reprojection errors.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "orb-slam-2"
  ],
  "paper_ids": [
    "2016-orb-slam-2"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2016-orb-slam-2"
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
  "entrypoint": "solution.pose_inliers",
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
    "evaluator_sha256": "7e0e38767904d6bc05c1f0f76c96b6cae96ef54a61382b4c4d7d59c969ff1f79"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1610.06475"
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

# Select Geometric Pose Inliers

Implement `pose_inliers(world_points, pixels, camera_from_world, intrinsics, pixel_std, valid, threshold)`.

Compare supplied camera-pose hypotheses using normalized geometric reprojection errors.

`world_points (N,3)` are float64 meters, `pixels (N,2)` float64 observed `(x,y)` pixels, `0<=N<=4096`. `camera_from_world (K,4,4)` contains proper float64 world-to-camera transforms, `1<=K<=64`, `K*N<=262144`. `intrinsics (4,)` is float64 `[fx,fy,cx,cy]` pixels with focal lengths >=1e-3. `pixel_std (N,)` is float64 in `[1e-3,100]` pixels; `valid (N,)` bool. `threshold` is a Python int/float in `[0,100]`, applied to dimensionless normalized SQUARED error, not pixel distance.

For each pose and valid point with camera z strictly >1e-6 m, project and compute squared_error=sum((predicted-observed)^2)/pixel_std^2. Unsupported points have +Inf. Inliers have supported squared_error<=threshold. Return `squared_error (K,N)`, `inliers (K,N)`, int64 `counts (K,)`, float64 `median_error (K,)` of inlier normalized squared errors (NaN if none), and Python int `best`. Select best by descending count, ascending median error, then pose index; return -1 if every count is zero.

No pose fitting, RANSAC, occlusion reasoning or automatic chi-square quantile is performed. The uncertainty and threshold are caller-supplied, and invalid-mask numeric inputs are still validated.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. World point `[[0.,0.,1.]]`, observed pixel `[[1.,0.]]`, identity pose, intrinsics `[1.,1.,0.,0.]`, std 1 and threshold 1: normalized squared error 1 and one inlier.
2. Add a second pose with camera-from-world x translation +1 m. Its projected pixel is `[1.,0.]`, giving zero error. Both hypotheses have one inlier, so the second pose wins on median error.

## Source and scope

[Primary source](https://arxiv.org/abs/1610.06475). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Project each pose hypothesis independently, fill unsupported errors with infinity, and compute evidence counts and inlier-only medians. O(KN) projection work with O(KN) output storage; median computation has the usual selection cost.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
