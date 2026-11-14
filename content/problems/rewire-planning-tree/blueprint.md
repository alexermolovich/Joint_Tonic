---
{
  "schema_version": 1,
  "problem_id": "rewire-planning-tree",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Rewire a Tree Without Creating Cycles",
  "summary": "Replace one planning-tree edge only if the proposed connection is feasible, cycle-free and strictly cheaper.",
  "type": "component",
  "difficulty": "hard",
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
  "entrypoint": "solution.rewire_tree",
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
    "evaluator_sha256": "bcd4b882dfc528974f0d11effb86f4ec5e88d66bdf22244b06bc6aa410a1d513"
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

# Rewire a Tree Without Creating Cycles

Implement `rewire_tree(parents, edge_costs, vertex, new_parent, connection_cost, feasible)`.

Replace one planning-tree edge only if the proposed connection is feasible, cycle-free and strictly cheaper.

`parents` is int64 `(N,)`, `edge_costs` float64 `(N,)`, `2<=N<=10000`. Node 0 is the only root: parent[0]=-1, edge_cost[0]=0. Every other parent lies in `[0,N)` and differs from its node; all nodes must connect to root without cycles. Edge costs are nonnegative normalized path-cost units. Invalid input trees raise ValueError.

`vertex` is a Python int in `[1,N)`, `new_parent` a Python int in `[0,N)`, `connection_cost` a Python int/float in `[0,1e6]`, and `feasible` is a Python bool certifying the entire proposed edge under the caller's collision model. No geometry is inferred. Root rewiring (`vertex=0`) is an invalid argument.

Compute original additive root costs. Change the edge iff feasible is true, new_parent is neither vertex nor its descendant, and `root_cost[new_parent]+connection_cost < root_cost[vertex]` strictly. A self/descendant proposal, infeasible edge, equal-cost edge or more expensive edge leaves the tree unchanged. Return fresh `parents` int64 `(N,)`, `edge_costs` float64 `(N,)`, `root_costs` float64 `(N,)` recomputed for the final tree, and Python bool `changed`, in a dictionary. Propagate changed costs to all descendants; preserve their edge lengths. Work should be O(N), without a recursive traversal that fails on long chains.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Parents `[-1,0,1,0]`, edge costs `[0.,5.,2.,1.]`, vertex `1`, new parent `3`, connection cost `1`, feasible True yield parents `[-1,3,1,0]`, edge costs `[0.,1.,2.,1.]`, root costs `[0.,2.,4.,1.]`, changed True.
2. With the same original tree, connecting vertex `1` beneath vertex `2` would form a cycle. Return unchanged parents and edges, root costs `[0.,5.,7.,1.]`, changed False.

## Source and scope

[Primary source](https://arxiv.org/abs/1005.0416). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Build child adjacency once and traverse from root to validate reachability and compute costs. Mark the proposed vertex subtree, apply the strict improvement rule, and traverse the final tree again when changed. O(N) time and memory; an iterative list traversal supports long chains.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
