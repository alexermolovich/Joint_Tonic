---
{
  "schema_version": 1,
  "problem_id": "window-episode-without-crossing-boundaries",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Window an Episode Without Crossing Boundaries",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.episode_windows",
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
      "episode_ids": "dimensionless IDs",
      "window": "frames",
      "stride": "frames"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "Rows are chronological; each episode is a contiguous run. Stride restarts at each run.",
    "batching": "episode_ids(N,) -> int64(K,window), including (0,window)."
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
    "evaluator_sha256": "1056c20807edcd37b4ea368b5e09a59854de4c4147f8cc83ef8c04f5adcf1b91"
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
  "summary": "Generate fixed-length row-index windows wholly contained in individual contiguous episodes.",
  "difficulty": "medium",
  "estimated_minutes": 25,
  "domains": [
    "Robotics foundations"
  ],
  "topics": [
    "sequence-data"
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

# Window an Episode Without Crossing Boundaries

Generate fixed-length row-index windows wholly contained in individual contiguous episodes.

```python
def episode_windows(episode_ids, window, stride):
```

## Contract

Episode IDs are nonnegative integer-valued numbers; an ID may not reappear after its run ends. window and stride must be positive Python or NumPy integers (not bool), each <=10000. Produce windows in row order; starts are run_start + k*stride, keeping only complete windows. An empty input is valid. No padding or window crossing is allowed.

**Shapes and outputs:** episode_ids(N,) -> int64(K,window), including (0,window).

**Units:** episode_ids: dimensionless IDs, window: frames, stride: frames. **Time:** Rows are chronological; each episode is a contiguous run. Stride restarts at each run.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `episode_ids=[4,4,4,8,8], window=2, stride=1` â†’ `[[0,1],[1,2],[3,4]]`.
2. `episode_ids=[1,1,1,1,2], window=3, stride=2` â†’ `[[0,1,2]]`; no partial window is returned.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
