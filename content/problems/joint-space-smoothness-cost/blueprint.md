---
{
  "schema_version": 1,
  "problem_id": "joint-space-smoothness-cost",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Build a Joint-Space Smoothness Cost",
  "summary": "Compute a discrete weighted joint-step cost and its exact gradient.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "trajopt"
  ],
  "paper_ids": [
    "2014-trajopt"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2014-trajopt"
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
  "entrypoint": "solution.smoothness_cost",
  "physical_contract": {
    "frames": [
      "Declared joint coordinates or a common right-handed world frame, as specified"
    ],
    "units": {
      "values": "Radians, seconds, meters and corresponding derivatives; normalized spaces explicitly identified"
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
      "Independent numerical mechanism",
      "Boundary and malformed inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "fc03ec37b1ea93d7fccbbbd6824a9d30bd0051d575016fba8d22e74279780e6d"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://rll.berkeley.edu/trajopt/ijrr/"
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

# Build a Joint-Space Smoothness Cost

Implement `smoothness_cost(path, weights)`.

Compute a discrete weighted joint-step cost and its exact gradient.

`path` is float64 `(T,D)` radians, `1<=T<=4096`, `1<=D<=16`; `weights` float64 `(D,)` are nonnegative inverse-radians-squared weights. Return `cost`: Python float sum over adjacent rows and joints of `weights*(path[t+1]-path[t])²`, and `gradient`: fresh float64 `(T,D)` derivative with respect to every joint sample. A single-row path has zero cost and gradient. This discrete cost assumes a fixed waypoint indexing convention: no time spacing is supplied or inferred, and it is not a velocity integral or a time-optimal objective. The diagonal weighting is a bounded original teaching choice.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Path `[[0.],[1.],[3.]]`, weight `[2.]` gives cost `10` and gradient `[[-4.],[-4.],[8.]]`.
2. Path `[[7.,-2.]]`, weights `[1.,3.]` gives cost zero and gradient `[[0.,0.]]`.

## Source and scope

[Primary source](https://rll.berkeley.edu/trajopt/ijrr/). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(TD) time and memory. Accumulate signed edge contributions into adjacent gradient rows; do not treat interior samples as independent one-sided endpoints.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
