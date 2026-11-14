---
{
  "schema_version": 1,
  "problem_id": "rt1-control-latency-dropouts",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Measure Closed-Loop Latency and Action Dropouts",
  "summary": "An inference that finishes after its control deadline is not equivalent to an action applied on time.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2022-rt-1",
    "policy-components"
  ],
  "paper_ids": [
    "2022-rt-1"
  ],
  "paper_sections": [
    "Original measurement exercise motivated by RT-1 control-time efficiency; no proprietary robot telemetry or published latency number is reproduced."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
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
  "entrypoint": "solution.control_latency_report",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "All times and deadline are milliseconds on one synchronized monotonic clock; rates dimensionless."
    },
    "axes": "observed_ms(T), applied_ms(T) -> latency_ms(T) and summary scalars",
    "timestamp_assumptions": "Each applied entry corresponds to exactly its observed entry; no timestamp matching is inferred.",
    "batching": "observed_ms(T), applied_ms(T) -> latency_ms(T) and summary scalars"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original measurement exercise motivated by RT-1 control-time efficiency; no proprietary robot telemetry or published latency number is reproduced.",
    "primary_urls": [
      "https://arxiv.org/abs/2212.06817"
    ],
    "paper_card": "research/papers/vla-embodied/2022-rt-1.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Measure Closed-Loop Latency and Action Dropouts

## Contract

`control_latency_report(observed_ms, applied_ms, deadline_ms)` receives equal nonempty vectors(T,), T<=10000, observation timestamps>=0 strictly increasing and applied timestamps either -1 (missing action) or >=their observation. Different applied timestamps need not increase. deadline_ms is a positive scalar<=1e6. Return dict latency_ms:float64(T,) using -1 for missing, dropout_rate:float, deadline_miss_rate:float, mean_latency_ms:float or None. Dropout is missing; deadline miss is missing OR latency>deadline. Both rates divide by T. Mean uses delivered actions only, None if none.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original measurement exercise motivated by RT-1 control-time efficiency; no proprietary robot telemetry or published latency number is reproduced.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
