---
{
  "schema_version": 1,
  "problem_id": "gp-support-interpolation",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Interpolate a Trajectory Between Support States",
  "summary": "Interpolate one constant-velocity GP support interval with fixed endpoint positions and velocities.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "gaussian-process-motion-planning"
  ],
  "paper_ids": [
    "2017-gaussian-process-motion-planning"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-gaussian-process-motion-planning"
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
  "entrypoint": "solution.interpolate_support",
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
    "evaluator_sha256": "358646e05e708a65de9d74dae1799145237654bec02973755ede120e1214aa42"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1707.07383"
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

# Interpolate a Trajectory Between Support States

Implement `interpolate_support(start, end, duration, fractions)`.

Interpolate one constant-velocity GP support interval with fixed endpoint positions and velocities.

`start` and `end` are float64 `(D,2)`, `1<=D<=16`, columns joint position in radians and velocity in rad/s. `duration` is a Python int/float in `[1e-3,100]` seconds. `fractions` is float64 `(Q,)`, `0<=Q<=4096`, values in `[0,1]` in any order; fraction u means elapsed time u*duration. Return fresh float64 `position (Q,D)` and `velocity (Q,D)` in a dictionary, using cubic Hermite interpolation:

`q(u)=(2*u**3-3*u**2+1)*q0+(u**3-2*u**2+u)*duration*v0+(-2*u**3+3*u**2)*q1+(u**3-u**2)*duration*v1`.

Velocity is the analytic derivative with respect to elapsed seconds: differentiate in u and divide by duration. Do not wrap angles, clip results or change query order. Empty queries are supported. This cubic is the conditional mean of the independent constant-velocity, white-acceleration GP given both endpoint states. It is not interpolation for arbitrary GP kernels and does not report uncertainty, collisions or dynamic feasibility.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Start `[[0.,0.]]`, end `[[1.,0.]]`, duration `2`, fractions `[0.5]` give position `[[0.5]]` and velocity `[[0.75]]`.
2. Start `[[0.,2.]]`, end `[[4.,2.]]`, duration `2`, fractions `[0.,0.5,1.]` give positions `[[0.],[2.],[4.]]` and velocities `[[2.],[2.],[2.]]`.

## Source and scope

[Primary source](https://arxiv.org/abs/1707.07383). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Evaluate the four basis polynomials and their derivatives for every fraction. Multiply velocity boundary terms by duration in position, then divide the entire fraction derivative by duration. O(QD) time and output memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
