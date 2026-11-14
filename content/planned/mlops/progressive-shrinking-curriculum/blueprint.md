---
{
  "schema_version": 1,
  "problem_id": "progressive-shrinking-curriculum",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Sample a Progressive-Shrinking Curriculum",
  "summary": "Sample a Progressive-Shrinking Curriculum",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2020-once-for-all"
  ],
  "paper_ids": [
    "2020-once-for-all"
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
  "entrypoint": "solution.sample_progressive_subnets",
  "physical_contract": {
    "frames": [
      "No spatial transform; preserve caller-supplied scenario/model identities"
    ],
    "units": {
      "depth": "layer count",
      "width": "channel count",
      "kernel": "odd spatial sample count",
      "seed": "unsigned 32-bit integer"
    },
    "axes": "int64(N,3), columns depth,width,kernel",
    "timestamp_assumptions": "No live timestamps; latency metrics are supplied durations only.",
    "batching": "int64(N,3), columns depth,width,kernel"
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
    "evaluator_sha256": "b6ca28ef31a4a6542a9731ecdcdc8629db17bae58232b1ceb537801e66958569",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1908.09791"
    ],
    "paper_card": "research/papers/mlops-sim2real/2020-once-for-all.md",
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

# Sample a Progressive-Shrinking Curriculum

Implement sample_progressive_subnets(depths, widths, kernels, phase, count, seed) -> np.ndarray.

Each choice input is a Python list of1–16 strictly decreasing unique built-in non-bool positive ints: depths<=16, widths<=256, odd kernels<=9. phase is a built-in int in[0,3], count in[0,10000], seed in[0,2**32-1]. Phase0 allows only the largest choice for all axes. Phase1 enables every kernel, phase2 additionally every width, phase3 additionally every depth. Choices retain their provided decreasing order.

Construct an independent np.random.Generator(np.random.PCG64(seed)). Draw one array U=rng.random((count,3)), including all three coordinates even when an axis has one legal choice. Columns are depth,width,kernel. Choose index floor(U[:,axis]*len(allowed_axis)) independently. Return fresh int64(count,3), no input mutation or global RNG changes. Empty count yields shape(0,3). Invalid types/order/bounds raise ValueError.

This fixed phase order is an original teaching schedule. It encodes progressive eligibility, not OFA's exact optimizer/distillation/sandwich sampling or performance. Widths are channel counts; all choices are dimensionless architecture integers.
