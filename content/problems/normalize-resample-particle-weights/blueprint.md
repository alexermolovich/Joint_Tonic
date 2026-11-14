---
{
  "schema_version": 1,
  "problem_id": "normalize-resample-particle-weights",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Normalize and Resample Particle Weights",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.resample_particles",
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
      "weights": "unnormalized likelihood mass",
      "offset": "dimensionless unit-interval fraction"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "All particles describe the same state timestamp; no motion update is performed.",
    "batching": "weights(N,), 1<=N<=100000, scalar offset -> (float64 normalized(N,), int64 ancestry(N,))."
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
    "evaluator_sha256": "ab89b6220071c2327b1243edce266aab9c743d54b24cc6485e5a7855be39a8e5"
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
  "summary": "Normalize nonnegative particle weights and perform deterministic systematic resampling.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "state-estimation"
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

# Normalize and Resample Particle Weights

Normalize nonnegative particle weights and perform deterministic systematic resampling.

```python
def resample_particles(weights, offset):
```

## Contract

Weights must be nonnegative with positive total. Offset must be a scalar in [0,1). Divide by the maximum weight before summing to avoid underflow. Systematic positions are (offset+arange(N))/N. Return the first cumulative-weight index strictly greater than each position (searchsorted side="right"); force the last cumulative entry to 1 to absorb roundoff. Zero-weight particles must never be selected at an exact boundary. This function must not draw random numbers.

**Shapes and outputs:** weights(N,), 1<=N<=100000, scalar offset -> (float64 normalized(N,), int64 ancestry(N,)).

**Units:** weights: unnormalized likelihood mass, offset: dimensionless unit-interval fraction. **Time:** All particles describe the same state timestamp; no motion update is performed.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `weights=[1,0,2,1], offset=0.5` â†’ normalized `[0.25,0,0.5,0.25]`, ancestry `[0,2,2,3]`.
2. `weights=[0,5], offset=0` â†’ normalized `[0,1]`, ancestry `[1,1]`; a position of zero skips zero mass.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.

Numerical endpoint convention: clamp computed systematic positions to np.nextafter(1.0,0.0), because floating arithmetic can round a nominally subunit position to 1. This keeps ancestry indices in range.
