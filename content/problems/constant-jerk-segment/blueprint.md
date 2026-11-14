---
{
  "schema_version": 1,
  "problem_id": "constant-jerk-segment",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Integrate a Constant-Jerk Motion Segment",
  "summary": "Integrate one constant-jerk segment for several rotational joints.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "ruckig"
  ],
  "paper_ids": [
    "2021-ruckig"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2021-ruckig"
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
  "entrypoint": "solution.integrate_jerk",
  "physical_contract": {
    "frames": [
      "Declared joint coordinates or a common right-handed world frame, as specified"
    ],
    "units": {
      "values": "Radians, seconds, meters and corresponding derivatives; normalized spaces explicitly identified"
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
      "Independent numerical mechanism",
      "Boundary and malformed inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "7439b599f669312a6e3dc348a3d742b90b129d304e766f32571afead74709ed0"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2105.04830"
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

# Integrate a Constant-Jerk Motion Segment

Implement `integrate_jerk(position, velocity, acceleration, jerk, duration)`.

Integrate one constant-jerk segment for several rotational joints.

The four float64 arrays have shape `(D,)`, `1<=D<=64`: position is radians, velocity radians/second, acceleration radians/second², and jerk radians/second³. All joint axes are independent coordinates of the same robot; no spatial transform occurs. `duration` is a Python int/float in `[0,100]` seconds, measured from the supplied common start time. Return a dict of fresh float64 `(D,)` arrays: `position=q+v*t+a*t²/2+j*t³/6`, `velocity=v+a*t+j*t²/2`, `acceleration=a+j*t`. Duration zero returns independent copies of the initial state. This integrates a supplied segment; it does not choose switching times, enforce joint limits, or implement Ruckig's time-optimal search.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Initial `q=v=a=[0.]`, jerk `[2.]`, duration `0.5` gives position `[1/24]`, velocity `[0.25]`, acceleration `[1.]` in the stated units.
2. Initial `q=[1.]`, `v=[2.]`, `a=[3.]`, jerk `[4.]`, duration `0` returns `[1.]`, `[2.]`, `[3.]` in fresh arrays.

## Source and scope

[Primary source](https://arxiv.org/abs/2105.04830). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(D) time and output memory. Compute the three polynomials independently from the initial state; do not update acceleration before using its original value in velocity.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
