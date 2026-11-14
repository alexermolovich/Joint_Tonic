---
{
  "schema_version": 1,
  "problem_id": "build-robot-sequence-validity-masks",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Build Padding and Validity Masks for Robot Sequences",
  "type": "function",
  "paper_ids": [],
  "entrypoint": "solution.sequence_masks",
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
      "lengths": "frames",
      "max_steps": "frames"
    },
    "axes": "No spatial axes are transformed.",
    "timestamp_assumptions": "One common monotonic clock in seconds.",
    "batching": "lengths(B,) -> valid bool(B,T), attention bool(B,T,T), T=max_steps."
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
    "evaluator_sha256": "ab19c22a7c2fafcc2e94474cf5a8c0030a6349f1ecf4e9f4e659aa888ef42883"
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
  "summary": "Build valid-token and causal-attention masks for padded robot episodes.",
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

# Build Padding and Validity Masks for Robot Sequences

Build valid-token and causal-attention masks for padded robot episodes.

```python
def sequence_masks(lengths, max_steps):
```

## Contract

Lengths must be nonnegative integer-valued entries <=max_steps. max_steps is an integer in [0,512], not bool. B<=128. A token is valid when its index is less than its episode length. Attention[b,i,j] is true exactly when both i and j are valid and j<=i. True means allowed, not blocked. Empty batches and zero-length episodes are valid.

**Shapes and outputs:** lengths(B,) -> valid bool(B,T), attention bool(B,T,T), T=max_steps.

**Units:** lengths: frames, max_steps: frames. **Time:** One common monotonic clock in seconds.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[2,0], max_steps=3` â†’ valid `[[True,True,False],[False,False,False]]`; the first attention matrix is the table above, the second is all false.
2. `lengths=[1], max_steps=1` â†’ valid `[[True]]`, attention `[[[True]]]`.

## Evaluation and visualization plan

Public tests exercise the two worked examples. Hidden tests cover declared edge cases, validation, and independent invariants. Theory provides an accessible static trace. No real hardware is actuated.

## Reproducibility

Use the pinned worker and deterministic original fixtures. Version this contract before changing numerical or error behavior.
