---
{
  "schema_version": 1,
  "problem_id": "log-sinkhorn-assignments",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Normalize Assignments with Sinkhorn Iterations",
  "summary": "Normalize a positive transport assignment by alternating row and column updates in log space.",
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
    "feature-matching-score-matrix"
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
  "entrypoint": "solution.sinkhorn_assignments",
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
    "evaluator_sha256": "c3830d855e363495aaeeb761b6dc93834dbf6e3822e3cad9c287c1673bc90c57"
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

# Normalize Assignments with Sinkhorn Iterations

Implement `sinkhorn_assignments(log_scores, row_mass, column_mass, iterations)`.

Normalize a positive transport assignment by alternating row and column updates in log space.

`log_scores` is float64 `(N,M)`, `1<=N,M<=128`, entries with absolute magnitude <=100. `row_mass (N,)` and `column_mass (M,)` are float64, each entry in `[1e-9,1]`; each vector sum must be within absolute tolerance 1e-9 of 1, then normalize each vector to sum exactly 1 numerically. `iterations` is a Python int in `[1,200]`.

Initialize row and column log-potentials to zero. Repeat exactly the requested number of iterations, updating all rows first and all columns second: `u=log(a)-logsumexp(S+v,axis=columns)`, then `v=log(b)-logsumexp(S+u,axis=rows)`. Inputs already contain entropy-scaled logits; no additional temperature is applied.

Return a dictionary: `log_transport (N,M)=S+u[:,None]+v[None,:]`, `transport (N,M)=exp(log_transport)`, and Python floats `row_error=max(abs(transport.sum(1)-a))`, `column_error=max(abs(transport.sum(0)-b))`. Use stable log-sum-exp. The final update enforces column marginals up to floating error; row marginals may still have residual error after finite iterations. Do not silently iterate to convergence.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Zero `2x2` logits with row/column masses `[0.5,0.5]` give transport `[[0.25,0.25],[0.25,0.25]]` after one iteration.
2. Zero `2x2` logits with row masses `[0.75,0.25]` and column masses `[0.5,0.5]` give `[[0.375,0.375],[0.125,0.125]]`. Its logarithm is returned separately.

## Source and scope

[Primary source](https://arxiv.org/abs/1911.11763). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Maintain log-potentials instead of repeatedly scaling an exponentiated extreme matrix. Each iteration performs one row and one column log-sum-exp. O(iterations*N*M) time and O(NM+N+M) memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
