---
{
  "schema_version": 1,
  "problem_id": "dustbin-partial-assignment",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Reject Unmatched Features with Dustbins",
  "summary": "Give unmatched image features their own transport capacity and diagnose dustbin-dominant assignments.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "superglue"
  ],
  "paper_ids": [
    "2019-superglue"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2019-superglue"
  ],
  "prerequisite_problem_ids": [
    "log-sinkhorn-assignments"
  ],
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
  "entrypoint": "solution.dustbin_assignment",
  "physical_contract": {
    "frames": [
      "Image pixel coordinates x right, y down; feature channels dimensionless"
    ],
    "units": {
      "values": "Pixels for geometry, dimensionless confidence and descriptors"
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
    "evaluator_sha256": "f852b9be880d3c8ddc1fb19302461de43bd5070e16e00eeefecd880a12e97569"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1911.11763"
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

# Reject Unmatched Features with Dustbins

Implement `dustbin_assignment(scores, dustbin_score, iterations)`.

Give unmatched image features their own transport capacity and diagnose dustbin-dominant assignments.

`scores` is float64 `(N,M)`, `1<=N,M<=128`, absolute values <=100. `dustbin_score` is a Python int/float in `[-100,100]`; `iterations` is a Python int in `[1,200]`. Scores and masses are dimensionless.

Augment scores to `(N+1,M+1)` by filling the final row and column, including their shared corner, with dustbin_score. Row masses are `[1,...,1,M]/(N+M)`; column masses are `[1,...,1,N]/(N+M)`. Starting from zero log-potentials, perform exactly iterations row-then-column log-Sinkhorn updates as in the prerequisite. Multiply the resulting unit-mass transport matrix by `(N+M)`.

Return this fresh float64 matrix as `assignment`, plus bool `row_unmatched (N,)` when that row's dustbin-column value is strictly greater than every real-column value, and bool `column_unmatched (M,)` analogously for the dustbin row. Ties favor real feature indices, so equality does not mean unmatched. This diagnostic rejects dustbin-dominant rows/columns; it does not extract reciprocal matches. Fixed iteration count can leave row-mass residuals; no automatic convergence or geometric verification is implied.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One source and one target feature, real score 0 and dustbin score 0: every entry of the `2x2` assignment is 0.5. Both unmatched flags are False because the real and dustbin values tie.
2. One source and one target, real score -2 and dustbin score 0, 100 iterations: real-real and dustbin-corner values approach `1/(1+e)`; the two off-diagonal values approach `e/(1+e)`. Both feature unmatched flags are True.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Build the augmented score matrix and unequal bin capacities, solve the fixed log-Sinkhorn recurrence, then compare the bin entry against real assignments. O(iterations*(N+1)*(M+1)) time and O(NM) memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
