---
{
  "schema_version": 1,
  "problem_id": "relocalization-landmark-coverage",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Evaluate a Relocalization Candidate",
  "summary": "Evaluate relocalization candidates using distinct geometric landmarks and image coverage.",
  "type": "component",
  "difficulty": "medium",
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
    "reprojection-pose-hypothesis-inliers"
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
  "entrypoint": "solution.relocalization_coverage",
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
    "evaluator_sha256": "9c1b41478f55cdf8cf8a832bdb3d3886a28851b76c2d23a27405390a5c4cc6a6"
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

# Evaluate a Relocalization Candidate

Implement `relocalization_coverage(keypoints, landmark_ids, inliers, image_size, grid_size, min_landmarks, min_cells)`.

Evaluate relocalization candidates using distinct geometric landmarks and image coverage.

`keypoints (N,2)` is float64 `(x,y)` pixels, `0<=N<=4096`, within the closed center domain `[0,width-1] x [0,height-1]`. `landmark_ids (K,N)` is int64, `1<=K<=128`, entries -1 (unmatched) or 0..1_000_000_000. `inliers (K,N)` is bool; every True must refer to a nonnegative landmark ID. `image_size` is int64 `[height,width]`, each 1..4096; `grid_size` int64 `[rows,columns]`, each 1..64. `min_landmarks` is a Python int in 1..4096; `min_cells` a Python int in 1..grid_rows*grid_columns.

For each candidate, keep only its geometrically inlier feature observations. Deduplicate landmark IDs by retaining the lowest feature index for each ID. Count distinct landmark representatives and the grid cells occupied by THESE representatives. Cell indices are `row=floor(y*grid_rows/height)`, `column=floor(x*grid_columns/width)`.

Return int64 `unique_landmarks (K,)`, int64 `covered_cells (K,)`, bool `eligible (K,)` requiring both counts >=their thresholds, int64 `order (E,)` sorted by descending unique-landmark count, descending cell count and ascending candidate index, and Python int `best` first eligible or -1. No evidence yields zero counts and no eligible candidate. This is an original operational gate over supplied geometric inliers, not place recognition, pose estimation or a full ORB-SLAM2 relocalizer.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Keypoints `[[0.,0.],[3.,3.]]` in a `[4,4]` image and `[2,2]` grid, candidate landmark IDs `[[7,7]]`, both geometric inliers: unique_landmarks=1 and covered_cells=1. Only feature index 0 represents landmark 7.
2. Change IDs to `[[7,8]]`: both counts become 2. With min_landmarks=2 and min_cells=2 this candidate becomes eligible; the duplicated-ID candidate does not.

## Source and scope

[Primary source](https://arxiv.org/abs/1610.06475). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Keep the first inlier feature for each landmark ID, count its image cells, then rank eligible candidates. O(KN log N+K log K) time using sorted uniqueness; O(N+K) working memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
