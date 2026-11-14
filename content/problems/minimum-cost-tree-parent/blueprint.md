---
{
  "schema_version": 1,
  "problem_id": "minimum-cost-tree-parent",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Choose a Collision-Free Minimum-Cost Tree Parent",
  "summary": "Choose a parent from supplied path-feasible connections by cumulative cost.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "rrt-star"
  ],
  "paper_ids": [
    "2010-rrt-star"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2010-rrt-star"
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
  "entrypoint": "solution.choose_tree_parent",
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
    "evaluator_sha256": "4cab044c871c6b715e9524015872b8f48b9a5b41a1fd41023273519923a41697"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1005.0416"
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

# Choose a Collision-Free Minimum-Cost Tree Parent

Implement `choose_tree_parent(root_costs, edge_costs, feasible)`.

Choose a parent from supplied path-feasible connections by cumulative cost.

`root_costs` and `edge_costs` are float64 `(N,)`, `0<=N<=100000`, nonnegative in one common caller-defined path-cost unit. `feasible` is bool `(N,)`: True means the connecting path has already passed the caller's collision and neighborhood checks, not merely its endpoint. Return a dict `parent`: Python int index minimizing root_cost+edge_cost over feasible candidates, with lowest index breaking exact ties; `total_cost`: Python float of that sum. When no feasible candidate exists, return parent -1 and total_cost positive infinity. This explicit nonfinite output is a missing-parent sentinel; all input costs must still be finite. No coordinates, angular wrapping, timestamps, collision queries or tree mutation occur in this selection step.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Root costs `[3.,1.,2.]`, edge costs `[1.,4.,2.]`, all feasible gives totals `[4.,5.,4.]`: parent0 and total_cost4, using the lower index for a tie.
2. Root costs `[0.,5.]`, edge costs `[0.,1.]`, feasible `[False,False]` returns parent -1 and total_cost +infinity. An infeasible cheap connection cannot become a parent.

## Source and scope

[Primary source](https://arxiv.org/abs/1005.0416). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(N) time and memory. Add root and edge costs, replace infeasible totals by infinity, and select the first minimum only when a feasible candidate exists.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
