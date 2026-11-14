---
{
  "schema_version": 1,
  "problem_id": "relative-odometry-edges",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Construct Relative Pose Measurements from Local Odometry",
  "summary": "`relative_odometry(poses, times, edges)` poses(N,4,4),1<=N<=8192 are body-to-local-world transforms, translations meters; times(N) seconds strictly increasing, adjacent spacing>=1e-6; edges(E,2),0<=E<=32768, each0<=i<j<N; duplicates allowed, preserve edge order. Return transforms(E,4,4)=Ti^-1 Tj, durations(E)=tj-ti, speeds(E)=norm(relative_translation)/duration in m/s. Relative transform maps body-j coordinates into body-i; speeds are chord speed, not path speed. No scale estimation, time interpolation or pose optimization. Example local poses identity atx0 andx2, times[0,2],edge[0,1]=>relative translation[2,0,0],duration2,speed1. Example Ri=Rz90 at origin, Rj=I with world translation[1,0,0]=>relative rotationRz-90,translation[0,-1,0]. Empty edges preserves output shapes.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "vins-fusion"
  ],
  "paper_ids": [
    "2019-vins-fusion"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2019-vins-fusion"
  ],
  "prerequisite_problem_ids": [
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
  "entrypoint": "solution.relative_odometry",
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
    "evaluator_sha256": "f01f8d1899f62b9c355f47e7ab3c341c8bb84018441a882f8ccb69811760f611"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1901.03642"
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

# Construct Relative Pose Measurements from Local Odometry

Implement `relative_odometry(poses, times, edges)`.

`relative_odometry(poses, times, edges)` poses(N,4,4),1<=N<=8192 are body-to-local-world transforms, translations meters; times(N) seconds strictly increasing, adjacent spacing>=1e-6; edges(E,2),0<=E<=32768, each 0<=i<j<N; duplicates allowed, preserve edge order.

Return transforms(E,4,4)=Ti^-1 Tj, durations(E)=tj-ti, speeds(E)=norm(relative_translation) / duration in m/s.

Relative transform maps body-j coordinates into body-i; speeds are chord speed, not path speed.

No scale estimation, time interpolation or pose optimization.

Example: local poses identity at x=0 andx2, times[0,2],edge[0,1]=>relative translation[2,0,0],duration 2,speed 1.

Example: Ri=Rz90 at origin, Rj=I with world translation[1,0,0]=>relative rotationRz-90,translation[0,-1,0].

Empty edges preserves output shapes.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity rotations, local positions x=0 and x=2 meters at times 0 and 2 seconds, edge [0,1]: output translation [2,0,0], duration 2, chord speed 1 m/s.
2. First pose rotates 90 degrees about z at the origin; second has identity rotation and world position [1,0,0].

The relative rotation is -90 degrees about z and translation [0,-1,0].

## Source and scope

[Primary source](https://arxiv.org/abs/1901.03642).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute each relative rigid transform analytically, then divide translation norm by the positive time difference.

Time and output storage are O(E); input validation is O(N).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
