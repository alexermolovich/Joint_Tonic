---
{
  "schema_version": 1,
  "problem_id": "act-teleoperation-quality",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Detect Teleoperation Demonstration Quality Failures",
  "summary": "A demonstration can look smooth in video while its logged joint stream contains impossible jumps or missing observations.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-aloha-act",
    "policy-components"
  ],
  "paper_ids": [
    "2023-aloha-act"
  ],
  "paper_sections": [
    "Original demonstration-quality check motivated by ALOHA/ACT data collection. Thresholds are supplied; this is not a collision or contact-quality evaluator."
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
  "entrypoint": "solution.teleop_quality_flags",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Joint positions radians; times seconds; max_speed radians/second, one threshold per joint."
    },
    "axes": "times(T), joints(T,D), observed(T), bounds(D) -> three Boolean flags(T)",
    "timestamp_assumptions": "Time samples must be strictly increasing on one clock; differences are between adjacent recorded rows.",
    "batching": "times(T), joints(T,D), observed(T), bounds(D) -> three Boolean flags(T)"
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
    "authoring_notes": "Original demonstration-quality check motivated by ALOHA/ACT data collection. Thresholds are supplied; this is not a collision or contact-quality evaluator.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.13705"
    ],
    "paper_card": "research/papers/vla-embodied/2023-aloha-act.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Detect Teleoperation Demonstration Quality Failures

## Contract

`teleop_quality_flags(times,joints,observed,lower,upper,max_speed)` receives strictly increasing finite times(T,) in seconds, 1<=T<=4096; finite joints(T,D),1<=D<=64 in radians; observed:bool(T,); lower/upper/max_speed:(D,), lower<upper and max_speed>0. Return dict missing:bool(T,) = ~observed, out_of_range:bool(T,) for any joint outside inclusive limits, speed_jump:bool(T,) for any absolute finite difference divided by dt exceeding max_speed. speed_jump[0]=False. Evaluate range and speed on all rows independently of observed; observed only marks sensor completeness. Inputs can exceed the supplied joint ranges because finding those rows is the task.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original demonstration-quality check motivated by ALOHA/ACT data collection. Thresholds are supplied; this is not a collision or contact-quality evaluator.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
