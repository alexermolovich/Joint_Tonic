---
{
  "schema_version": 1,
  "problem_id": "time-parameterized-trajectory",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Interpolate a Time-Parameterized Trajectory",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.sample_trajectory",
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
      "robot joint coordinates"
    ],
    "units": {
      "times,queries": "seconds",
      "positions": "radians",
      "velocity": "radians/second"
    },
    "axes": "Each column is one joint with its declared positive rotation direction.",
    "timestamp_assumptions": "One common monotonic clock in seconds.",
    "batching": "times(T,), positions(T,D), queries(M,) -> float64 position(M,D), velocity(M,D)."
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
    "evaluator_sha256": "786aa11ca5b014120e1241255583158c53645b2637849b3e3f7939c0ed39b787"
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
  "summary": "Sample a piecewise-linear joint trajectory and its segment velocity at requested times.",
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

# Interpolate a Time-Parameterized Trajectory

Sample a piecewise-linear joint trajectory and its segment velocity at requested times.

```python
def sample_trajectory(times, positions, queries):
```

## Contract

T>=2, D>=1. Times must be strictly increasing. Queries may be unsorted or empty but must lie in [times[0],times[-1]]. Interpolate linearly. At an interior knot return the velocity of the segment to its right; at the final knot use the last segment. No angular wrapping, extrapolation, or smoothing.

**Shapes and outputs:** times(T,), positions(T,D), queries(M,) -> float64 position(M,D), velocity(M,D).

**Units:** times,queries: seconds, positions: radians, velocity: radians/second. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `times=[0,1,3], positions=[[0],[2],[4]], queries=[0.5,1,3]` â†’ positions `[[1],[2],[4]]`, velocities `[[2],[1],[1]]`.
2. `times=[0,2], positions=[[0,2],[4,0]], queries=[2,0]` â†’ positions `[[4,0],[0,2]]`, velocities `[[2,-1],[2,-1]]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Adjacent knot intervals must be at least 1e-9 seconds; smaller intervals raise ValueError.
