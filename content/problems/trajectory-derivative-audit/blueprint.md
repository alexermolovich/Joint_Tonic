---
{
  "schema_version": 1,
  "problem_id": "trajectory-derivative-audit",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Validate a Trajectory Against Derivative Limits",
  "summary": "Audit supplied trajectory derivative samples without claiming continuous-time feasibility.",
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
  "entrypoint": "solution.audit_derivatives",
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
    "evaluator_sha256": "e38727075f1d75b696e930a18ff368d8804eaf63bfce7dda5a9f3c74161833aa"
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

# Validate a Trajectory Against Derivative Limits

Implement `audit_derivatives(velocity, acceleration, jerk, limits)`.

Audit supplied trajectory derivative samples without claiming continuous-time feasibility.

Velocity, acceleration and jerk are float64 `(N,D)`, `0<=N<=4096`, `1<=D<=16`, in rad/s, rad/s² and rad/s³. Rows are synchronized samples at caller-declared times; the function compares supplied derivatives and does not estimate them by finite differences. `limits` is float64 `(3,D)`, rows velocity/acceleration/jerk, in matching units, with every bound at least `1e-9`. Return `violations`: fresh bool `(N,D,3)`, ordered velocity/acceleration/jerk on the last axis, True where absolute derivative is strictly greater than its bound. Return `max_ratio`: float64 `(3,D)` maximum absolute derivative divided by its limit over N (all zero for N=0), and `passed`: Python bool true iff N>0 and no violations. Equality passes; empty evidence never passes. This is a sampled audit, not a guarantee about values between samples.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One joint sample with velocity `2`, acceleration `-3`, jerk `4`, limits `[[2.],[3.],[4.]]` yields violations `[[[False,False,False]]]`, max ratios `[[1.],[1.],[1.]]`, passed True.
2. Change velocity to `2.2`: only its velocity flag is True, maximum velocity ratio is `1.1`, and passed is False.

## Source and scope

[Primary source](https://arxiv.org/abs/2105.04830). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(ND) time and memory. Stack derivative orders explicitly, compare absolute magnitudes, and preserve the difference between no evidence and evidence below the limit.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
