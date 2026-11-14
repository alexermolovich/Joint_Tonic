---
{
  "schema_version": 1,
  "problem_id": "mpc-tracking-cost",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Evaluate an MPC Tracking Cost",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.mpc_tracking_cost",
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
      "not-spatial"
    ],
    "units": {
      "states,targets": "declared state units",
      "controls": "declared actuator units",
      "weights": "inverse squared corresponding units",
      "cost": "dimensionless"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "State rows 0..N; control row k applies between states k and k+1, with no dt multiplier in this discrete objective.",
    "batching": "states/targets(N+1,D), controls(N,M), state_weights/terminal_weights(D,), control_weights(M,) -> Python float."
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
    "evaluator_sha256": "2050f716d59fa0e164f856d26940f9130d576cc03a0f13629cb45afcbdc91d4a"
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
  "summary": "Score a finite-horizon predicted trajectory with stage, control-effort, and terminal penalties.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "planning-control"
  ],
  "paper_sections": [],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "perception_completion"
  ]
}
---

# Evaluate an MPC Tracking Cost

Score a finite-horizon predicted trajectory with stage, control-effort, and terminal penalties.

```python
def mpc_tracking_cost(states, targets, controls, state_weights, control_weights, terminal_weights):
```

## Contract

D,M>=1; N may be zero. Weight vectors are nonnegative and represent diagonal quadratic penalties. Sum state tracking errors at k=0..N-1 and controls at k=0..N-1; apply terminal_weights only to final state k=N. Targets have exactly the same shape as states. No terminal double-counting or timestep factor.

**Shapes and outputs:** states/targets(N+1,D), controls(N,M), state_weights/terminal_weights(D,), control_weights(M,) -> Python float.

**Units:** states,targets: declared state units, controls: declared actuator units, weights: inverse squared corresponding units, cost: dimensionless. **Time:** State rows 0..N; control row k applies between states k and k+1, with no dt multiplier in this discrete objective.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `states=[[1],[2],[3]], targets=zeros((3,1)), controls=[[1],[2]], state_weights=[1], control_weights=[2], terminal_weights=[3]` â†’ `42.0`.
2. `states=[[2,-1]], targets=[[0,0]], controls=empty((0,1)), state_weights=[9,9], control_weights=[1], terminal_weights=[2,3]` â†’ `11.0`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
