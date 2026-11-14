---
{
  "schema_version": 1,
  "problem_id": "loop-closure-consistency-gate",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Reject Inconsistent Loop Closures",
  "summary": "`gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed)` residuals(K,6),0<=K<=8192, translationmeters+rotationradians supplied same tangent convention; covariance(K,6,6),symmetricatol1e-9 thenaverage,positive eigenvalues satisfy lambda_min>=max(1e-9,lambda_max*1e-8). overlap(K)fraction[0,1],elapsed(K)seconds[0,1e6];thresholdscalar[0,1e6]on squaredMahalanobis,min_overlap[0,1],min_elapsed[0,1e6]. Return squared_distance(K)=r.Tsolve(C,r),accepted(K)=(d<=threshold)&(overlap>=min)&(elapsed>=min),reason int64(K) priority1 elapsed too short,2 overlap low,3 Mahalanobis too large,0 accepted. All values validated even rejected for earlierreasons. Covariance cross terms matter. Original operational consistency gate for supplied registration evidence; not LIO-SAM's actual ICP fitness heuristic, a probability guarantee, or loop proposal/registration. Example r=[2,0,0,0,0,0],C=I,threshold4,overlap.5,min.5,elapsed10,min10=>d4accepted. Exampleelapsed9 andoverlap0 andlargeerror=>reason1; empty arrayscorrectshapes. Covariance entry C[i,j] has the product of residual coordinate i and j units (m\u00b2, m\u00b7rad, or rad\u00b2).",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "lio-sam"
  ],
  "paper_ids": [
    "2020-lio-sam"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2020-lio-sam"
  ],
  "prerequisite_problem_ids": [
    "mahalanobis-measurement-gate"
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
  "entrypoint": "solution.gate_loop_closures",
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
    "evaluator_sha256": "32d625c0f4ea3b9d1432eb63bf3d165226b0d93d6b8dcaa9457bad291d111bac"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2007.00258"
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

# Reject Inconsistent Loop Closures

Implement `gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed)`.

`gate_loop_closures(residuals, covariance, overlap, elapsed, threshold, min_overlap, min_elapsed)` residuals(K,6),0<=K<=8192, translation meters + rotation radians supplied same tangent convention; covariance(K,6,6),symmetric atol1e-9  then average,positive eigenvalues satisfy lambda_min>=max(1e-9,lambda_max*1e-8). overlap(K)fraction[0,1],elapsed(K)seconds[0,1e6];thresholdscalar [0,1e6]on squared Mahalanobis,min_overlap[0,1],min_elapsed[0,1e6].

Return squared_distance(K)=r.Tsolve(C,r),accepted(K)=(d<=threshold)&(overlap>=min)&(elapsed>=min),reason int64(K) priority1 elapsed too short,2 overlap low,3 Mahalanobis too large,0 accepted.

All values validated even rejected for earlier reasons.

Covariance cross terms matter.

Original operational consistency gate for supplied registration evidence; not LIO-SAM's actual ICP fitness heuristic, a probability guarantee, or loop proposal/registration.

Example: r=[2,0,0,0,0,0],C=I,threshold4,overlap.5,min.5,elapsed10,min10=>d4accepted.

Example: elapsed9 andoverlap0 andlarge error=>reason 1; empty arrayscorrectshapes.

Covariance entry C[i,j] has the product of residual coordinate i and j units (m², m·rad, or rad²).

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Residual [2,0,0,0,0,0], identity covariance, overlap 0.5, elapsed 10 seconds, and gates (4,0.5,10) give squared distance 4, accepted True, reason 0.

Boundaries are inclusive.
2. A candidate with elapsed 9, overlap 0 and large residual receives reason 1 when minimum elapsed is 10: the temporal reason takes precedence over the other failures.

## Source and scope

[Primary source](https://arxiv.org/abs/2007.00258).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Validate and symmetrize covariance roundoff, solve each six-dimensional linear system, and apply inclusive gates with explicit reason precedence. O(K) time/storage for fixed six-coordinate residuals.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
