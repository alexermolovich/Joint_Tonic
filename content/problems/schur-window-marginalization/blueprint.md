---
{
  "schema_version": 1,
  "problem_id": "schur-window-marginalization",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Marginalize a Visual-Inertial Window with a Schur Complement",
  "summary": "Eliminate old state variables from a fixed linearized estimator window while preserving its quadratic information.",
  "type": "component",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "vins-mono"
  ],
  "paper_ids": [
    "2017-vins-mono"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-vins-mono"
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
  "entrypoint": "solution.marginalize_window",
  "physical_contract": {
    "frames": [
      "Explicit world, body, camera or dimensionless scaled-state frame in the contract"
    ],
    "units": {
      "values": "Meters, seconds, radians, pixels, or dimensionless normalized quantities as defined per argument"
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
    "evaluator_sha256": "69ec088ceb283be63a53eaa6957cd411f97448b4931dc68cc43d6876125782e7"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1708.03852"
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

# Marginalize a Visual-Inertial Window with a Schur Complement

Implement `marginalize_window(normal_matrix, rhs, retained)`.

Eliminate old state variables from a fixed linearized estimator window while preserving its quadratic information.

`normal_matrix` is float64 `(D,D)` and `rhs` float64 `(D,)`, `2<=D<=96`. `retained` is a Python int in `1..D-1`; the first retained coordinates are kept and the rest removed. Parameter coordinates are already dimensionless and scaled. The declared normal equations are H*delta=rhs; rhs is not implicitly negated.

Require H symmetric within atol=1e-9, rtol=0, then replace it by `(H+H.T)/2`. Its eigenvalues must satisfy `lambda_min>=max(1e-8,lambda_max*1e-8)`. Gauges and regularization are therefore already handled, with condition number at most 1e8. Partition H into aa,ab,ba,bb blocks and rhs into a,b.

Return a dictionary with `normal=Haa-Hab@solve(Hbb,Hba)`, `reduced_rhs=rhs_a-Hab@solve(Hbb,rhs_b)`, `retained_step=solve(normal,reduced_rhs)`, `removed_step=solve(Hbb,rhs_b-Hba@retained_step)`, and Python float `constant_shift=-0.5*rhs_b.T@solve(Hbb,rhs_b)`. Output shapes are `(A,A)`, `(A,)`, `(A,)`, `(D-A,)`, respectively. The shift is the constant in the reduced quadratic `0.5*x_a.T@normal@x_a-reduced_rhs.T@x_a+constant_shift`. Do not form matrix inverses. This eliminates one fixed linearization; it does not update a marginalized prior after changing nonlinear linearization points.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. H=`[[2.,1.],[1.,2.]]`, rhs=`[1.,0.]`, retained=1: reduced normal `[[1.5]]`, reduced rhs `[1.]`, retained step `[2/3]`, removed step `[-1/3]`, constant shift 0.
2. H=diag(2,4), rhs=`[2.,8.]`, retained=1: reduced normal `[[2.]]`, reduced rhs `[2.]`, steps `[1.]` and `[2.]`, constant shift -8.

## Source and scope

[Primary source](https://arxiv.org/abs/1708.03852). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Solve once for the eliminated block response to retained coordinates and once for its response to rhs. Form the reduced system, solve it, and back-substitute. Dense O(D^3) time and O(D^2) memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
