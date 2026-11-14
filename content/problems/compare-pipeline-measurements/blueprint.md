---
{
  "schema_version": 1,
  "problem_id": "compare-pipeline-measurements",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compare Black-Box and Grey-Box Pipeline Measurements",
  "summary": "Compare Black-Box and Grey-Box Pipeline Measurements",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2023-robotperf"
  ],
  "paper_ids": [
    "2023-robotperf"
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
  "entrypoint": "solution.compare_pipeline_measurements",
  "physical_contract": {
    "frames": [
      "No spatial transform; named records retain their supplied identity"
    ],
    "units": {
      "timestamps": "integer nanoseconds on one monotonic clock",
      "durations": "integer nanoseconds"
    },
    "axes": "Independent request IDs; each stage span belongs to exactly one request.",
    "timestamp_assumptions": "Timestamps use one supplied monotonic clock; no live clock or resampling.",
    "batching": "Independent request IDs; each stage span belongs to exactly one request."
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
    "evaluator_sha256": "01e869afacb7138482acdc3bdcc1d2967b9da4f400a017220b0da2b3fc012ffa",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2023-robotperf](https://arxiv.org/abs/2309.09212). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/2309.09212"
    ],
    "paper_card": "research/papers/mlops-sim2real/2023-robotperf.md",
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

# Compare Black-Box and Grey-Box Pipeline Measurements

Implement compare_pipeline_measurements(boundaries, spans) -> list[tuple[str,int,int,int,int]].

boundaries is a Python list of 0–10000 tuples(request_id,start_ns,end_ns), unique request IDs. spans is a list of 0–100000 tuples(request_id,stage_id,start_ns,end_ns), at most one span per(request_id,stage_id). IDs match ASCII [a-z][a-z0-9_-]{0,63}. All timestamps are built-in non-bool ints in [0,2**63-1], start<=end, on the same caller-declared clock. Every span names a known request and lies wholly within its boundary interval. Empty/zero-duration spans are valid.

For each request, return(request_id,boundary_ns,covered_ns,unobserved_ns,overlap_ns) in ASCII request-ID order. boundary_ns=end-start. covered_ns is the length of the union of its half-open spans. unobserved_ns=boundary_ns-covered_ns. overlap_ns is the sum of individual span durations minus covered_ns; triple overlaps count their extra multiplicity. A request without spans has zero coverage and its full boundary duration unobserved. Validate the entire input, preserve it, and raise ValueError for malformed types, duplicate IDs/spans, unknown requests, bounds or inconsistent intervals. All numeric outputs are built-in ints.

Unobserved time is not automatically queue time; overlap is not automatically wasted work. Instrumentation coverage and probe overhead require separate interpretation. No clock synchronization or causal critical-path reconstruction occurs.
