---
{
  "schema_version": 1,
  "problem_id": "palm-e-sensor-readiness",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Validate Missing-Modality and Stale-Sensor Inputs",
  "summary": "A tensor with the right shape may still describe the robot\u2019s past.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-palm-e",
    "policy-components"
  ],
  "paper_ids": [
    "2023-palm-e"
  ],
  "paper_sections": [
    "Original deployment input gate motivated by embodied multimodal models. It does not impute a missing modality or establish spatial calibration validity."
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
  "entrypoint": "solution.sensor_readiness",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "All timestamps and ages are seconds on one synchronized clock; sensors retain caller-declared calibration/frame."
    },
    "axes": "presence/timestamps(B,M), now(B), max_age/required(M) -> flags(B,M), ready(B)",
    "timestamp_assumptions": "Boundary age=max_age is usable; future sensor stamps are not usable. No clock correction is performed.",
    "batching": "presence/timestamps(B,M), now(B), max_age/required(M) -> flags(B,M), ready(B)"
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
    "authoring_notes": "Original deployment input gate motivated by embodied multimodal models. It does not impute a missing modality or establish spatial calibration validity.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.03378"
    ],
    "paper_card": "research/papers/vla-embodied/2023-palm-e.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Validate Missing-Modality and Stale-Sensor Inputs

## Contract

`sensor_readiness(present,timestamps,now,max_age,required)` takes present:bool(B,M),1<=B<=64,1<=M<=32; timestamps:real(B,M) seconds>=0; now:real(B,) seconds>=0; max_age:real(M,) seconds>=0; required:bool(M,). Return dict usable:bool(B,M), stale:bool(B,M), ready:bool(B,). A present sensor is stale when timestamp>now or now-timestamp>max_age. Missing sensors have stale=False and usable=False. usable=present&~stale. A row is ready iff every required sensor is usable; if none required, ready=True even with no present sensor. Validate all timestamps including missing entries.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original deployment input gate motivated by embodied multimodal models. It does not impute a missing modality or establish spatial calibration validity.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
