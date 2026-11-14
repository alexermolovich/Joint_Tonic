---
{
  "schema_version": 1,
  "problem_id": "detr-hungarian-assignment",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Match Object Queries with the Hungarian Algorithm",
  "summary": "Match Object Queries with the Hungarian Algorithm",
  "type": "function",
  "difficulty": "hard",
  "estimated_minutes": 35,
  "domains": [
    "perception"
  ],
  "topics": [
    "detr",
    "paper-component"
  ],
  "paper_ids": [
    "2020-detr"
  ],
  "paper_sections": [
    "Mechanism and conventions defined in theory.md"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "detr-matching-cost"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build",
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
  "entrypoint": "solution.match_queries",
  "physical_contract": {
    "frames": [
      "Explicit caller-observation conventions in statement"
    ],
    "units": {
      "features": "dimensionless"
    },
    "axes": "cost(Q,M),1<=Q<=128,0<=M<=Q; result(M,), indexed by target.",
    "timestamp_assumptions": "One observation batch; no internal clock.",
    "batching": "cost(Q,M),1<=Q<=128,0<=M<=Q; result(M,), indexed by target."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-9,
    "atol": 1e-7,
    "public_case_families": [
      "worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "validation",
      "edge-policy",
      "layout",
      "preservation",
      "independent-oracle",
      "scale"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching task. No copied source code or figure.",
    "primary_urls": [
      "https://arxiv.org/abs/2005.12872"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_implementation"
  ],
  "reviewers": ["vla_implementation"]
}
---

# Match Object Queries with the Hungarian Algorithm

## Contract

Implement match_queries(cost). cost is a finite NumPy float64 array (Q,M),1<=Q<=128,0<=M<=Q, abs values<=1e6. Return new NumPy int64 query_for_target(M,): each target j gets one query index in[0,Q), all selected query indices distinct, minimizing sum(cost[query_for_target[j],j]). Any globally optimal assignment is accepted when costs tie; do not assume a lexicographic tie requirement. Empty targets return shape(0,). Preserve inputs and support noncontiguous arrays. TypeError for non-array cost; ValueError for other violations. Implement a polynomial assignment algorithm using Python/NumPy; SciPy is not installed. Target order is preserved; unused queries are not returned. Costs are dimensionless matching objectives for one image, not probabilities or timestamps. Optimal objective comparisons use atol1e-7,rtol1e-9; index validity is exact.

## Implementation and proof

Independent review precedes implementation. Test both examples and documented invalid/empty/layout cases; use independent objective/shape/value oracles. Verify actual isolated public Run and hidden Submit plus starter negative control. Reference and fixture code are original. Theory includes original math and static numerical/layout table with text alternative. No full-paper reproduction is claimed.
