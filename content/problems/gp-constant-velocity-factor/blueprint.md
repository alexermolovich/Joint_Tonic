---
{
  "schema_version": 1,
  "problem_id": "gp-constant-velocity-factor",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build a Gaussian-Process Smoothness Factor",
  "summary": "Build one independent-joint constant-velocity Gaussian-process prior factor.",
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
  "entrypoint": "solution.gp_motion_factor",
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
    "evaluator_sha256": "ccb3a97b7286791e64f2f6cdee25500c26cdfd10f25f3a7419eafba648eb7f39"
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

# Build a Gaussian-Process Smoothness Factor

Implement `gp_motion_factor(start, end, duration, spectral_density)`.

Build one independent-joint constant-velocity Gaussian-process prior factor.

`start` and `end` are float64 `(D,2)`, `1<=D<=16`, with columns joint position in radians and velocity in rad/s. They are synchronized support states of the same rotational joints; no angle wrapping occurs. `duration` is a Python int/float in `[1e-3,100]` seconds. `spectral_density` is float64 `(D,)` in `[1e-6,1e6]`, measured in rad²/s³.

For each joint form residual `e=[q1-q0-duration*v0, v1-v0]` and covariance `Q=qc*[[duration**3/3,duration**2/2],[duration**2/2,duration]]`. Compute the lower Cholesky factor `L` with positive diagonal and the whitened residual `solve(L,e)`. Return a dictionary with fresh float64 `residual (D,2)`, `covariance (D,2,2)`, `whitened (D,2)`, and Python float `cost=0.5*sum(whitened**2)`. Covariance entries have units rad², rad²/s and rad²/s² by block; whitened residuals and cost are dimensionless. This is the independent-joint constant-velocity prior used as a GPMP2 component; it does not optimize a path or include obstacle factors.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Start and end `[[0.,0.]]`, duration `1`, spectral density `[1.]` yield residual `[[0.,0.]]`, covariance `[[[1/3,1/2],[1/2,1]]]`, whitened residual zero and cost `0`.
2. Start `[[0.,0.]]`, end `[[1.,0.]]`, duration `1`, density `[1.]` yield residual `[[1.,0.]]`, whitened `[[sqrt(3),-3]]`, and cost `6`.

## Source and scope

[Primary source](https://arxiv.org/abs/1707.07383). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Construct the physical residual before whitening. Solve with a lower Cholesky factor, never with the covariance itself: the squared residual norm must equal the inverse-covariance quadratic form. O(D) time and output memory because every factor is 2×2.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
