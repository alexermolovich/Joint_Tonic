---
{
  "schema_version": 1,
  "problem_id": "linearized-collision-penalty",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Linearize a Signed-Distance Collision Penalty",
  "summary": "Evaluate a local first-order clearance model, hinge penalties, and one chosen subgradient.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "trajopt"
  ],
  "paper_ids": [
    "2014-trajopt"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2014-trajopt"
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
  "entrypoint": "solution.linearized_collision_penalty",
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
    "evaluator_sha256": "dff859983b86226324dad8958143f9365d7899ad657c6269ddcb05ff9f297f7b"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://rll.berkeley.edu/trajopt/ijrr/"
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

# Linearize a Signed-Distance Collision Penalty

Implement `linearized_collision_penalty(distances, jacobian, step, margin)`.

Evaluate a local first-order clearance model, hinge penalties, and one chosen subgradient.

`distances` float64 `(N,)` meters and `jacobian` float64 `(N,D)` meters/radian are sampled at one current joint configuration, `0<=N<=4096`, `1<=D<=16`. `step` float64 `(D,)` is a proposed joint increment in radians; `margin` is Python int/float `[0,100]` meters. Positive clearance means outside collision. Return `predicted`: float64 `(N,)` equal to distances+jacobian@step; `hinge`: float64 `(N,)` max(margin-predicted,0); `cost`: Python float sum(hinge); and `gradient`: float64 `(D,)` negative sum of Jacobian rows whose predicted clearance is strictly below margin. At exact equality choose subgradient zero. Empty pairs give empty predicted/hinge and zero cost/gradient. All outputs are fresh. The supplied Jacobian is not recomputed; the result describes the local model, not verified nonlinear scene clearance.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Distances `[0.02,0.08]`, Jacobian `[[1.],[-1.]]`, step `[0.01]`, margin `0.05`: predicted `[0.03,0.07]`, hinge `[0.02,0.]`, cost `0.02`, gradient `[-1.]`.
2. Distance `[0.05]`, Jacobian `[[2.]]`, step `[0.]`, margin `0.05`: hinge and cost zero, chosen gradient `[0.]` at the kink.

## Source and scope

[Primary source](https://rll.berkeley.edu/trajopt/ijrr/). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(ND) time and memory. Compute the affine clearance prediction, select strictly active hinges, then sum their negative Jacobian rows.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
