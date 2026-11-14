---
{
  "schema_version": 1,
  "problem_id": "pullback-motion-metric",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Pull Back a Local Motion Metric",
  "summary": "Pull one supplied natural-form task policy into normalized joint coordinates.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "rmpflow"
  ],
  "paper_ids": [
    "2018-rmpflow"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2018-rmpflow"
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
  "entrypoint": "solution.pullback_policy",
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
    "evaluator_sha256": "1bc5833667e5f6702dcd952468a5ace4028cca92423fbfcdd42d9522ff17a30b"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1811.07049"
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

# Pull Back a Local Motion Metric

Implement `pullback_policy(jacobian, jacobian_rate, joint_velocity, task_metric, task_force)`.

Pull one supplied natural-form task policy into normalized joint coordinates.

`jacobian` and `jacobian_rate` are float64 `(T,D)`, `1<=T,D<=16`. `joint_velocity` is `(D,)`, `task_metric` `(T,T)`, and `task_force` `(T,)`. Joint and task coordinates are normalized dimensionless coordinates with a fixed caller-defined scaling; J is dimensionless, its time derivative Jdot is 1/s, velocity is 1/s, and natural force is 1/s². The metric is dimensionless. All inputs describe one synchronized state; the force is a supplied natural-form policy value, not a physical Newton force.

Validate M against its transpose with atol=1e-10, rtol=0, then symmetrize. Compute its eigenvalues; reject any less than -1e-10, clip accepted negative eigenvalues to zero, and reconstruct the effective metric. This numerical PSD normalization is part of the contract. Return fresh float64 `metric (D,D) = J.T @ M @ J` and `force (D,) = J.T @ (f - M @ Jdot @ joint_velocity)` in a dictionary. Do not omit the curvature correction, invert a metric or generate leaf policies. An exactly zero task metric is allowed; task_force remains an independent supplied input.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. J=`[[2.]]`, Jdot=`[[1.]]`, joint velocity `[3.]`, metric `[[4.]]`, force `[20.]` give pulled metric `[[16.]]` and force `[16.]`: subtract the task curvature contribution `4*1*3=12` before multiplying by J.T.
2. With the same inputs but Jdot=`[[0.]]`, pulled metric remains `[[16.]]`, while force becomes `[40.]`.

## Source and scope

[Primary source](https://arxiv.org/abs/1811.07049). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Validate and normalize the task metric, compute the task-map curvature Jdot*v, subtract its metric-weighted contribution, and multiply back with J.T. The metric follows the quadratic-form pullback. O(T³+T²D+TD²) time; no inverse is needed.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
