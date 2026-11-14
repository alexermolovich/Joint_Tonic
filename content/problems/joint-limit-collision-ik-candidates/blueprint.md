---
{
  "schema_version": 1,
  "problem_id": "joint-limit-collision-ik-candidates",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Enforce Joint Limits and Collision Constraints in IK",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.select_safe_ik_candidate",
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "physical_contract": {
    "frames": [
      "fixed right-handed base xy plane"
    ],
    "units": {
      "lengths,obstacles,target,margin": "metres",
      "candidates,joint_limits": "radians"
    },
    "axes": "Two +z revolute joints; second angle is relative. Obstacles are circles in the base plane.",
    "timestamp_assumptions": "Each candidate is a static configuration; paths between candidates are not checked.",
    "batching": "lengths(2,), candidates(N,2), limits(2,2), obstacles(K,3), target(2,), scalar margin -> dict or None."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-input",
      "independent-oracle",
      "immutability"
    ],
    "performance_class": "cpu",
    "evaluator_sha256": "40ece62ab1359a18874cc8a04270b4c2bb1d5a8c6e75e12deec9f9f80b8260ec"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [],
    "implementation_urls": []
  },
  "summary": "Reject planar IK candidates violating joint limits or link-obstacle clearance, then rank the survivors.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "inverse-kinematics"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "serial-chain-forward-kinematics"
  ],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Enforce Joint Limits and Collision Constraints in IK

Reject planar IK candidates violating joint limits or link-obstacle clearance, then rank the survivors.

```python
def select_safe_ik_candidate(lengths, candidates, joint_limits, obstacles, target, margin):
```

## Contract

Lengths positive, N<=1000, K<=100. Limits rows [lower,upper] require lower<=upper; boundaries are allowed. Obstacles rows [center_x,center_y,radius] require radius>=0. Margin>=0 inflates each obstacle. A candidate collides if the minimum Euclidean distance from either closed link segment to any center is <=radius+margin; touching counts as collision. Reject candidates outside either joint range without clipping. Among survivors choose smallest Euclidean endpoint-target distance, with exact ties choosing lower input index. Return exactly {"index": Python int,"q":float64(2,),"point":float64(2,),"error":Python float}; return None if none survive. Empty arrays retain (0,2)/(0,3) shapes. Validate all inputs even if an early winner exists.

**Shapes and outputs:** lengths(2,), candidates(N,2), limits(2,2), obstacles(K,3), target(2,), scalar margin -> dict or None.

**Units:** lengths,obstacles,target,margin: metres, candidates,joint_limits: radians. **Time:** Each candidate is a static configuration; paths between candidates are not checked.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[1,1], candidates=[[0,0],[pi/2,0]], joint_limits=[[-pi,pi],[-pi,pi]], obstacles=empty((0,3)), target=[2,0], margin=0` selects index0, q `[0,0]`, point `[2,0]`, error0.
2. Add obstacle `[0.5,0,0.1]`. Candidate0 crosses it, so select index1 with point approximately `[0,2]` and error `sqrt(8)`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Each link length must be at least 1e-9 metres; smaller values raise ValueError.
