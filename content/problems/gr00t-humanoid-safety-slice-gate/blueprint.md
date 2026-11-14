---
{
  "schema_version": 1,
  "problem_id": "gr00t-humanoid-safety-slice-gate",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Gate a Humanoid Policy Release on Safety Slices",
  "summary": "Gate a Humanoid Policy Release on Safety Slices.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2025-gr00t-n1",
    "policy-components"
  ],
  "paper_ids": [
    "2025-gr00t-n1"
  ],
  "paper_sections": [
    "Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification."
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
  "entrypoint": "solution.humanoid_release_gate",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Latency milliseconds; counts are evaluation trials/incidents, success rates dimensionless. Required slices are explicitly chosen scenario/embodiment conditions."
    },
    "axes": "Explicit batch, time, embodiment and channel axes defined in the contract",
    "timestamp_assumptions": "Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time.",
    "batching": "Explicit batch, time, embodiment and channel axes defined in the contract"
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
    "authoring_notes": "Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.",
    "primary_urls": [
      "https://arxiv.org/abs/2503.14734"
    ],
    "paper_card": "research/papers/vla-embodied/2025-gr00t-n1.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Gate a Humanoid Policy Release on Safety Slices

## Contract

Integer vectors trials,successes,safety_incidents(S,),1<=S<=128,0<=successes,incidents<=trials<=1e6; p95_latency_ms real(S,)nonnegative; required bool(S,); at least one required slice. min_trials integer scalar1..1e6,min_success_rate real0..1,max_latency_ms real0..1e6. Return success_rate float64(S,) NaNwherezero trials; slice_pass bool(S,), failures list ofS lists ofreason strings in order insufficient_trials,safety_incident,low_success,latency; and release bool ALL required slices pass. slice_pass evaluates every slice, even optional ones; optional failures do not block release. Low_success applies ifftrials>0 and rate<minimum. Incident count>0 fails; equality at success/latency thresholds passes. Insufficient trial slices may have other reasons too. This is a synthetic deterministic evidence gate, NOT a physical safety guarantee or statistical confidence bound.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
