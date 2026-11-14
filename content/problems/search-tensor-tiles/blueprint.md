---
{
  "schema_version": 1,
  "problem_id": "search-tensor-tiles",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Search Tensor Tile Sizes with a Toy Cost Model",
  "summary": "Search Tensor Tile Sizes with a Toy Cost Model",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2018-tvm"
  ],
  "paper_ids": [
    "2018-tvm"
  ],
  "paper_sections": [
    "Mechanism described in theory; bounded teaching contract"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; local bubblewrap baseline",
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
  "entrypoint": "solution.select_tensor_tile",
  "physical_contract": {
    "frames": [
      "No spatial transform; named records retain their supplied identity"
    ],
    "units": {
      "memory_bytes": "bytes",
      "shape": "matrix element counts",
      "launch_cost": "dimensionless toy cost units",
      "cost": "dimensionless toy cost units"
    },
    "axes": "A(M,K) @ B(K,N); candidate order is (tm,tn,tk).",
    "timestamp_assumptions": "No wall-clock timestamps; deterministic logical inputs only.",
    "batching": "A(M,K) @ B(K,N); candidate order is (tm,tn,tk)."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-09,
    "atol": 1e-10,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-oracle",
      "edge-shapes",
      "invalid-contract",
      "preservation",
      "scale"
    ],
    "evaluator_sha256": "4e1d58b379206cb2d1319488b38ef700eb09f0aa5bdac516fbe049700847f4b0",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://www.usenix.org/conference/osdi18/presentation/chen"
    ],
    "paper_card": "research/papers/mlops-sim2real/2018-tvm.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Search Tensor Tile Sizes with a Toy Cost Model

Implement select_tensor_tile(shape, candidates, memory_bytes, launch_cost) -> tuple | None.

shape=(M,N,K), positive built-in non-bool ints <=4096, describes A(M,K)B(K,N). candidates is a list of 1–4096 unique tuples(tm,tn,tk), positive built-in ints <=256. memory_bytes is a built-in int in[1,2**31]; launch_cost is a built-in int in[0,10**9]. Each candidate uses a teaching float32 tile footprint F=4*(tm*tk+tk*tn+tm*tn) bytes. It is feasible when F<=memory_bytes; tile sizes may exceed a matrix dimension and use padding.

Let Q=ceil(M/tm)*ceil(N/tn)*ceil(K/tk). The ORIGINAL toy cost is C=Q*(tm*tn*tk+launch_cost), counting padded scalar multiply-accumulate units and tile launches. Select minimum(C,F,tm,tn,tk) lexicographically among feasible candidates. Return(tm,tn,tk,C,F), all built-in ints; return None when none fit. Validate all candidates even when an earlier one already wins. Preserve inputs. All malformed inputs raise ValueError.

These costs are dimensionless teaching scores, not measured cycles, latency, real cache use, or TVM's learned cost model. The footprint assumes one A,B,C tile with no double buffering; full matrix storage is outside this candidate model.
