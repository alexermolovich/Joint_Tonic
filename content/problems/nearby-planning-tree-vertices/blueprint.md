---
{
  "schema_version": 1,
  "problem_id": "nearby-planning-tree-vertices",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Find Nearby Planning Tree Vertices",
  "summary": "Find tree vertices inside an inclusive weighted configuration-space radius.",
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
  "entrypoint": "solution.nearby_vertices",
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
    "evaluator_sha256": "7d022bba16fe682830a082b22a104b085f6e8e32587fd15cf424f9be63430732"
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

# Find Nearby Planning Tree Vertices

Implement `nearby_vertices(vertices, query, weights, radius)`.

Find tree vertices inside an inclusive weighted configuration-space radius.

`vertices` float64 `(N,D)`, `0<=N<=100000`, `1<=D<=16`; `query` float64 `(D,)`; `weights` float64 `(D,)` with values >=1e-9. All coordinates and weights are dimensionless normalized configuration features, already scaled consistently upstream. `radius` is Python int/float in `[0,1e6]` in the resulting dimensionless metric. Squared distance is sum(weights*(vertex-query)²). Return `(indices, distances)`: fresh int64 `(K,)` original indices with squared distance <=radius², in ascending index order, and float64 `(K,)` square-root distances for those indices. Do not sort by distance. Empty vertices return empty outputs. There is no angular wrapping, collision check, timestamp dependence, or RRT* radius schedule in this component.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Vertices `[[0.,0.],[1.,0.],[0.,2.]]`, query `[0.,0.]`, weights `[4.,1.]`, radius2 gives indices `[0,1,2]` and distances `[0.,2.,2.]`; boundary vertices are included.
2. Vertices `[[1.],[0.],[0.]]`, query `[0.]`, weight `[1.]`, radius0 gives indices `[1,2]`, distances `[0.,0.]`, preserving duplicates and index order.

## Source and scope

[Primary source](https://arxiv.org/abs/1005.0416). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

O(ND) time and memory. Compute one squared distance per row, filter by an inclusive radius, and preserve original index order.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
