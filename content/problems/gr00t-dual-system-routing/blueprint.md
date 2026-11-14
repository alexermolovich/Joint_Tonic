---
{
  "schema_version": 1,
  "problem_id": "gr00t-dual-system-routing",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Route Inputs Through a Dual-System Policy Interface",
  "summary": "Route Inputs Through a Dual-System Policy Interface.",
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
  "entrypoint": "solution.route_dual_system",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates."
    },
    "axes": "Explicit batch, time, embodiment and channel axes defined in the contract",
    "timestamp_assumptions": "Physical timestamps and maximum context age are seconds on one synchronized monotonic clock; no cross-device clock correction.",
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

# Route Inputs Through a Dual-System Policy Interface

## Contract

context real(B,C), state real(B,S),1<=B<=64,1<=C,S<=64; embodiment_ids integer(B,), state_projectors real(G,S,E),1<=G<=16,1<=E<=64, IDs0..G-1. context_time/observation_time real(B,) seconds>=0; max_context_age real scalar0..1e6 seconds. Project each state row using its embodiment-specific matrix and concatenate unchanged context then projected state: conditioning float64(B,C+E). Return conditioning, head_ids int64(B,) copy of embodiment_ids, ready bool(B,), context_age float64(B,)=observation-context time. Ready iff0<=age<=max_context_age. Future/stale context is reported not raised; conditioning is still returned for inspection and must NOT be executed when readyFalse. This routes already encoded features; no asynchronous runtime, model inference or implicit context refresh.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
