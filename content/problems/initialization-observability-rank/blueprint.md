---
{
  "schema_version": 1,
  "problem_id": "initialization-observability-rank",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Detect Unobservable Initialization Motion",
  "summary": "Diagnose unsupported parameter directions in a supplied linearized visual-inertial initialization system.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "vins-mono"
  ],
  "paper_ids": [
    "2017-vins-mono"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-vins-mono"
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
  "entrypoint": "solution.initialization_rank",
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
    "evaluator_sha256": "2c2144c0a6cc0dbfdfe8098c56df6474563c8f1c2e4fe5cbe5fc81ad966f2377"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1708.03852"
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

# Detect Unobservable Initialization Motion

Implement `initialization_rank(jacobian, parameter_scales, measurement_std, relative_cutoff)`.

Diagnose unsupported parameter directions in a supplied linearized visual-inertial initialization system.

`jacobian` is float64 `(R,D)`, `0<=R<=4096`, `1<=D<=32`, absolute entries <=1000. `parameter_scales (D,)` and `measurement_std (R,)` are float64 in `[1e-6,1000]`. `relative_cutoff` is a Python int/float in `[1e-12,0.01]`. The Jacobian rows are measurement sensitivities after known gauge freedoms have already been removed. Each column's parameter and each row's measurement may have different physical units: J has measurement units per parameter unit, scales have their corresponding parameter units, and standard deviations have their corresponding measurement units.

Form dimensionless A=J*parameter_scales[None,:]/measurement_std[:,None]. Compute its singular values in descending order, padded with zeros to length D. Retain values strictly greater than relative_cutoff times the largest singular value. All-zero A has rank zero.

Return a dictionary with `singular_values (D,)`, Python int `rank`, Python bool `observable` iff rank==D, Python float `condition` equal to largest/smallest singular value if full rank and +Inf otherwise, and `unobservable_projector (D,D)=I-Vr.T@Vr`, where Vr contains retained right singular vectors as rows. The projector operates in dimensionless scaled parameter coordinates. With no rows, return zero singular values, rank 0 and the identity projector. This diagnostic concerns the supplied local linearization; it is not VINS-Mono's exact motion heuristic or a proof of global nonlinear observability.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. J=`[[2.,0.],[0.,1.]]`, scales and standard deviations all 1, cutoff 0.001: singular values `[2.,1.]`, rank 2, condition 2 and zero unobservable projector.
2. J=`[[1.,0.]]` with unit scales/std gives rank 1, singular values `[1.,0.]`, condition +Inf and projector `[[0.,0.],[0.,1.]]`. The second scaled parameter direction has no measurement support.

## Source and scope

[Primary source](https://arxiv.org/abs/1708.03852). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Whiten and scale each Jacobian entry, compute a thin SVD, pad its singular spectrum, and form the null projector from retained right singular vectors. O(RD^2+D^3) time and O(RD+D^2) storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
