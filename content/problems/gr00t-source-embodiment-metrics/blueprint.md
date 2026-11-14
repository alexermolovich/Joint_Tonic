---
{
  "schema_version": 1,
  "problem_id": "gr00t-source-embodiment-metrics",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Report Metrics by Source and Embodiment",
  "summary": "Report Metrics by Source and Embodiment.",
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
  "entrypoint": "solution.source_embodiment_metrics",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Latency milliseconds; source/embodiment labels are fixed evaluation schema indices; success is binary closed-loop trial outcome."
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

# Report Metrics by Source and Embodiment

## Contract

source_ids integer(N,)0realrobot,1humanvideo,2syntheticrobot; embodiment_ids integer(N,) in0..E-1, E=num_embodiments integer1..16; success bool(N,); latency_ms real(N,)nonnegative;0<=N<=10000. All rows are labelled evaluation records already assigned to a target robot embodiment; video-source evaluation uses an explicit adapted robot test, not inferred video actions. Return count int64(3,E), success_rate float64(3,E), p95_latency_ms float64(3,E); no records gives NaN for both metrics. p95 nearest rank ceil(.95*n)-1 WITHIN each cell. Also overall_success float (allNmean) or None ifempty, and worst_observed_success float(minfinite cell rate) or None. Counts include failed trials, no source reweighting.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
