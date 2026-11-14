---
{
  "schema_version": 1,
  "problem_id": "isaac-gym-steady-state-throughput",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Measure Simulation and Learning Throughput",
  "summary": "Compilation and initialization can dominate a short simulator benchmark.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "simulation-evaluation",
    "2021-isaac-gym"
  ],
  "paper_ids": [
    "2021-isaac-gym"
  ],
  "paper_sections": [
    "Selected operational or evaluation mechanism; simplified scope in Theory"
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
  "entrypoint": "solution.simulation_throughput",
  "physical_contract": {
    "frames": [
      "Fixed caller-defined axes; no implicit coordinate transform"
    ],
    "units": {
      "timestamps/duration": "integer nanoseconds",
      "steps_per_second": "completed environment transitions/second",
      "updates_per_second": "learner updates/second"
    },
    "axes": "Chronological iteration vectors(N,), aggregate scalars.",
    "timestamp_assumptions": "Integer nanoseconds on one synchronized monotonic clock",
    "batching": "Chronological iteration vectors(N,), aggregate scalars."
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
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "84e0e7c9936ad628869e4a0f3201d8efd2c4c4688db3a411c0601413e2935856"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full simulator or benchmark reproduction. Backlog PB-280",
    "primary_urls": [
      "https://arxiv.org/abs/2108.10470"
    ],
    "paper_card": "research/papers/simulation-sim2real/2021-isaac-gym.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Measure Simulation and Learning Throughput

## Goal

Compilation and initialization can dominate a short simulator benchmark.

## Contract

simulation_throughput(start_ns, end_ns, environment_steps, learner_updates, warmup) -> dict{duration_ns,environment_steps,learner_updates,steps_per_second,updates_per_second}. Four arrays int64(N,),0<=N<=100000. Timestamp endpoints nonnegative<=2^63-1 on ONE synchronized monotonic clock; require start<end each row and end[i]<=start[i+1] in supplied chronological order. Counts each0..1e9. warmup built-in int0..N excludes first warmup complete iterations. Sum measured iteration durations (end-start), not gaps between rows; exclude launch/compilation warmup. Return Python-int sums; total durations must use arbitrary precision after exact per-row integer subtraction. Rates float count*1e9/duration. If no rows remain, duration/counts0, both ratesNaN. Environment steps already count all environments and action repeats; never multiply again by B. This is serialized evidence aggregation, not asynchronous GPU timing or real benchmarking.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

start=[0,2000000000],end=[1000000000,4000000000],steps=[100,400],updates=[1,6],warmup=1 -> duration2000000000,steps400,updates6,steps_per_second200,updates_per_second3.

### Example 2

The same input with warmup=2 -> all totals0 and both ratesNaN.

## Source and scope

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
