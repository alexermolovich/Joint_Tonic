---
{
  "schema_version": 1,
  "problem_id": "graph-throughput-jitter",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Measure Throughput and Jitter Across a ROS-Style Graph",
  "summary": "Measure Throughput and Jitter Across a ROS-Style Graph",
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
  "entrypoint": "solution.graph_throughput_jitter",
  "physical_contract": {
    "frames": [
      "No spatial transform; named records retain their supplied identity"
    ],
    "units": {
      "timestamps": "integer nanoseconds on one monotonic clock",
      "throughput": "events per second",
      "mean_interval_ns": "nanoseconds",
      "jitter_ns": "population standard deviation in nanoseconds"
    },
    "axes": "One ordered event list per named stage; no spatial axes.",
    "timestamp_assumptions": "Timestamps use one supplied monotonic clock; no live clock or resampling.",
    "batching": "One ordered event list per named stage; no spatial axes."
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
    "evaluator_sha256": "61a80c4621bc57719fb6261654f4753f52cec5f087fc2f8b547dbdafab8c2540",
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

# Measure Throughput and Jitter Across a ROS-Style Graph

Implement graph_throughput_jitter(completions, window) -> dict.

completions is a Python dict of 0–128 stage IDs matching ASCII [a-z][a-z0-9_-]{0,63}, each mapping to a nondecreasing Python list of built-in non-bool integer completion timestamps in [0,2**63-1]. Total timestamps <=100000. All stages use one synchronized monotonic clock. window is a tuple(start_ns,end_ns) of those integer bounds with start_ns<end_ns.

For each stage in ASCII ID order, include completions in the half-open interval [start_ns,end_ns). Return exactly count (built-in int), throughput_hz=count*1e9/(end_ns-start_ns), mean_interval_ns, jitter_ns in its new dict. With fewer than two retained events, both interval metrics are None. Otherwise form adjacent retained-event differences, take their arithmetic mean and population standard deviation (divide by number of intervals, not number minus one). Equal timestamps produce zero intervals. Subtract integers before converting differences to floats; timestamps can exceed exact float precision. Preserve all inputs. Invalid containers, IDs, ordering, types or bounds raise ValueError.

Stage throughput is not path latency, sensor rate, or causal request matching. Dropped events and clocks are not inferred; this function summarizes declared completed work only.
