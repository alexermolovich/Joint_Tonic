---
{
  "schema_version": 1,
  "problem_id": "bound-convex-trust-step",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Bound a Sequential Convex Trust-Region Step",
  "summary": "Project a proposed joint increment into a box trust region and position limits.",
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
  "entrypoint": "solution.bound_trust_step",
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
    "evaluator_sha256": "80bb2d7e5c5b57da2fc075a35b889905a6a4dde3badc08c53bf1bc25c94234ff"
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

# Bound a Sequential Convex Trust-Region Step

Implement `bound_trust_step(current, proposal, lower, upper, radius)`.

Project a proposed joint increment into a box trust region and position limits.

`current`, `proposal`, `lower`, `upper` are float64 `(D,)` radians, `1<=D<=64`, with lower<=current<=upper elementwise. Proposal is an increment, not an absolute configuration. `radius` is Python int/float in `[0,100]` radians. Intersect increment bounds `[-radius,radius]` with `[lower-current,upper-current]`, clip proposal to that intersection, and return a dict `step`: float64 `(D,)`, `next_configuration`: float64 `(D,)` current+step, and `clipped`: bool `(D,)` where proposal differs exactly from step. All outputs are independent. Radius0 yields zero step. Each joint is a rotational coordinate at the current planning iteration; no timestamp integration or angular wrapping is performed. This box projection bounds a proposed step; it does not solve a full constrained quadratic program or certify nonlinear constraints.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Current `[0.8,-0.8]`, proposal `[0.5,-0.5]`, lower `[-1.,-1.]`, upper `[1.,1.]`, radius `0.3` gives step approximately `[0.2,-0.2]`, next `[1.,-1.]`, and clipped `[True,True]`.
2. Current `[0.]`, proposal `[0.1]`, limits `[-1.]` to `[1.]`, radius `0` returns step `[0.]`, next `[0.]`, clipped `[True]`.

## Source and scope

[Primary source](https://rll.berkeley.edu/trajopt/ijrr/). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(D) time and memory. Intersect increment intervals before clipping; clipping an absolute target by the increment radius uses the wrong coordinate origin.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
