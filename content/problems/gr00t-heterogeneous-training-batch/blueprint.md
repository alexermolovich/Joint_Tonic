---
{
  "schema_version": 1,
  "problem_id": "gr00t-heterogeneous-training-batch",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Build a Heterogeneous Real, Video, and Synthetic Batch",
  "summary": "Build a Heterogeneous Real, Video, and Synthetic Batch.",
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
  "entrypoint": "solution.heterogeneous_batch",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates."
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

# Build a Heterogeneous Real, Video, and Synthetic Batch

## Contract

observations real(B,E),1<=B<=32,1<=E<=128; actions PythonlistB; source_ids integer(B,)0=realrobot,1=humanvideo,2=syntheticrobot; embodiment_ids integer(B,). Video rows must have actions=None and embodiment=-1. Real/synthetic rows require embodiment0..15 and real action matrix(Hi,Di),1<=Hi<=64,1<=Di<=32; all action rows supplied in caller-normalized embodiment channel order. Pad action dimensions/time to max Hi,Di across ROBOT rows; if no robot rows use(0,0). Return observations copy, actions float64(B,Hmax,Dmax) exact0padding, action_mask bool same shape true only supplied robot entries, source_ids/embodiment_ids int64copies. Human video may train another objective but contributes no invented actuator labels. Reject None robot actions and any numeric video actions.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.

## Deliberate training-scope difference

GR00T N1 uses learned latent-action targets extracted from human video and treats that representation as a separate embodiment. This exercise only collates direct robot actuator labels, so video rows have no action supervision here. A latent-action objective and its learned inverse-dynamics representation are out of scope; video rows are not claimed to be unused by the full paper.
