---
{
  "schema_version": 1,
  "problem_id": "sphere-signed-distance-cost",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Compute a Signed-Distance Collision Cost",
  "summary": "Score a batch of robot sphere approximations against spherical obstacles in one world frame.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "curobo"
  ],
  "paper_ids": [
    "2023-curobo"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2023-curobo"
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
  "entrypoint": "solution.sphere_collision_cost",
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
    "evaluator_sha256": "5c8c9361f2e1d3b69237c4640f54949848650cf8b6ea41ba26cdca3cd331ccc5"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.17274"
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

# Compute a Signed-Distance Collision Cost

Implement `sphere_collision_cost(centers, radii, obstacles, obstacle_radii, margin)`.

Score a batch of robot sphere approximations against spherical obstacles in one world frame.

`centers` is float64 `(B,S,3)`, `1<=B<=64`, `1<=S<=32`; `radii` float64 `(S,)`; `obstacles` float64 `(K,3)` and `obstacle_radii` float64 `(K,)`, `1<=K<=32`. All positions/radii are meters in the same right-handed world frame at one scene timestamp, and all radii are >=1e-9. `margin` is Python int/float in `[0,100]` meters. Sphere-pair separation is `d=norm(center-obstacle)-radius-obstacle_radius`, positive outside contact. Return fresh arrays `cost` float64 `(B,)`: sum of squared hinges `max(margin-d,0)²` over all sphere pairs; `clearance` float64 `(B,)`: minimum pair separation; `collision` bool `(B,)`: any pair with d<=0. Contact counts as collision even when margin0 produces zero hinge cost. This original sphere-sphere surrogate does not implement cuRobo's complete collision kernels or guarantee safety of a full robot mesh.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One robot sphere centered at `(0,0,0)` meters with radius 1, one obstacle at `(3,0,0)` radius 1, margin 2: clearance 1 m, cost 1 m², collision False.
2. Move the obstacle to `(2,0,0)` and set margin0: clearance zero, cost zero, collision True because the spheres touch.

## Source and scope

[Primary source](https://arxiv.org/abs/2310.17274). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(BSK) time and memory. Evaluate sphere-pair clearances before reducing cost, minimum clearance, and collision; each reduction has a different meaning.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
