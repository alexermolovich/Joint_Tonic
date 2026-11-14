---
{
  "schema_version": 1,
  "problem_id": "deskew-lidar-points",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Deskew a Lidar Scan with Motion Estimates",
  "summary": "Express points captured at different instants in one reference lidar frame using supplied per-point poses.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "lio-sam"
  ],
  "paper_ids": [
    "2020-lio-sam"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2020-lio-sam"
  ],
  "prerequisite_problem_ids": [
    "se3-transform-points",
    "compose-frame-transforms"
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
  "entrypoint": "solution.deskew_points",
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
    "evaluator_sha256": "99875fc71afa93d30f83d0666fecb256495b4a761d75c5dc2c49a064177428d4"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2007.00258"
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

# Deskew a Lidar Scan with Motion Estimates

Implement `deskew_points(points, world_from_capture, world_from_reference)`.

Express points captured at different instants in one reference lidar frame using supplied per-point poses.

`points` is float64 `(N,3)` meters, `0<=N<=8192`. `world_from_capture` is float64 `(N,4,4)`, where transform i maps the lidar frame at point i's capture time into a common world frame. `world_from_reference` is float64 `(4,4)`, mapping the desired reference lidar frame into the same world. All transforms must be proper rigid transforms with rotation/last-row checks atol=1e-9, rtol=0.

Return a fresh float64 `(N,3)` array in reference-lidar coordinates, using `inverse(world_from_reference) @ world_from_capture[i] @ homogeneous(points[i])`. The reference frame may be any caller-selected scan time; the poses already include the intended lidar extrinsic convention. Empty scans are valid. Pose estimates are supplied exactly aligned per point; do not infer timestamps, interpolate poses, integrate IMU data or estimate extrinsics. This geometric deskew component is distinct from applying one static transform to a synchronized cloud.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One captured point `[[2.,0.,0.]]`, capture pose with identity rotation and world translation `[1.,0.,0.]`, and identity reference pose yield `[[3.,0.,0.]]` in the reference lidar frame.
2. Change the reference pose's world translation to `[2.,0.,0.]`. The same capture and point now yield `[[1.,0.,0.]]` in the reference lidar frame.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Transform each point with its own capture pose, subtract the reference translation, and rotate by the reference inverse. Vectorize over points while preserving pose-to-point alignment. O(N) time and memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
