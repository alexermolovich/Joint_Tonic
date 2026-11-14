---
{
  "schema_version": 1,
  "problem_id": "roboturk-action-segments",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Detect Paused or Corrupted Action Segments",
  "summary": "Detect Paused or Corrupted Action Segments",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "operational-evidence",
    "2018-roboturk"
  ],
  "paper_ids": [
    "2018-roboturk"
  ],
  "paper_sections": [
    "Operational component discussed in Theory; explicit original teaching policy"
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
  "entrypoint": "solution.action_segment_report",
  "physical_contract": {
    "frames": [
      "Declared robot/session/feature identities; no implicit transform"
    ],
    "units": {
      "times_ns/duration_ns/min_duration_ns": "integer nanoseconds on one synchronized clock",
      "actions/max_command/deadband": "radians per second in supplied joint axes",
      "min_samples": "sample count"
    },
    "axes": "times(T,),actions(T,D),observed(T,),limits(D,),flags(T,); segments use half-open sample indices.",
    "timestamp_assumptions": "Supplied synchronized integer timestamps only where present; no wall clock",
    "batching": "times(T,),actions(T,D),observed(T,),limits(D,),flags(T,); segments use half-open sample indices."
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
    "evaluator_sha256": "f23bbb968348a964bf3d78414c729b56f30fdb9b8b396dae376480c79d4b68b2"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original operational teaching policy; no full paper API reproduction. Backlog PB-177",
    "primary_urls": [
      "https://arxiv.org/abs/1811.02790"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2018-roboturk.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "research_curator",
    "root"
  ]
}
---

# Detect Paused or Corrupted Action Segments

## Contract

`action_segment_report(times_ns, actions, observed, max_command, deadband, min_samples, min_duration_ns) -> dict`. times_ns is NumPy int64(T,),0<=T<=100000, values0..2^63-1 strictly increasing; actions NumPy float32/float64(T, D),1<=D<=32, at most 10^6 entries; NaN/Inf and any finite magnitudes are accepted as evidence. observed bool(T,), max_command float32/float64(D,) finite in(0,1e6]. deadband is finite built-in real in 0..min(max_command), min_samples built-in int in 1..100000, min_duration_ns built-in int in 0..2^63-1. Array dtypes/shapes and scalar contracts are validated; noncontiguous arrays are valid.

A corrupt row is unobserved OR has any nonfinite action OR any abs(action)>max_command. A pause candidate is a noncorrupt row with every abs(action)<=deadband. Find maximal contiguous candidate runs[start, end) in sample-index order. Mark a run paused only if end-start>=min_samples AND times_ns[end-1]-times_ns[start]>=min_duration_ns (exact integer ns). A corrupt row splits runs. Return corrupt:bool(T,), paused:bool(T,), segments:list[(start, end, duration_ns)] for qualifying maximal runs in order; tuple values Python ints. Empty T returns empty outputs. Actions are joint velocity commands in rad/s in caller-ordered actuator axes; no actual motion, contact or safety is inferred. Work O(TD).

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

times[0,10,20,30], actions[[0],[0],[1],[0]], all observed flags=True, max_command[2], deadband=0.1, min_samples=2, min_duration_ns=10 yields corrupt[F, F, F, F], paused[T, T, F, F], segments[(0,2,10)].

With times[0,10,20], actions[[0],[NaN],[0]], all observed flags=True, max_command[2], deadband=0.1, min_samples=2, min_duration_ns=0, corrupt[F, T, F], paused[F, F, F], segments[]. The corrupt row separates two short runs.

## Source and scope

Original bounded component inspired by [2018-roboturk](https://arxiv.org/abs/1811.02790). It does not reproduce the full paper or establish hardware safety or data-use authorization.
