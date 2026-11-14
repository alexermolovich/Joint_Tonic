---
{
  "schema_version": 1,
  "problem_id": "diffusion-denoising-budget",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Budget Denoising Steps Against Control Frequency",
  "summary": "More denoising iterations can improve a sampler while missing a robot deadline.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-diffusion-policy",
    "policy-components"
  ],
  "paper_ids": [
    "2023-diffusion-policy"
  ],
  "paper_sections": [
    "Original serving-budget exercise inspired by Diffusion Policy inference scheduling. A constant measured per-step cost is an explicit approximation, not a published timing guarantee."
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
  "entrypoint": "solution.denoising_budget",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Latency milliseconds; control frequency Hertz; counts dimensionless."
    },
    "axes": "candidate_steps(K) -> latency_ms(K), feasible(K), selected_steps scalar",
    "timestamp_assumptions": "One planning invocation per period1000/frequency_hz ms; overlap or amortization across action windows is outside this task.",
    "batching": "candidate_steps(K) -> latency_ms(K), feasible(K), selected_steps scalar"
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
    "authoring_notes": "Original serving-budget exercise inspired by Diffusion Policy inference scheduling. A constant measured per-step cost is an explicit approximation, not a published timing guarantee.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.04137"
    ],
    "paper_card": "research/papers/vla-embodied/2023-diffusion-policy.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Budget Denoising Steps Against Control Frequency

## Contract

`denoising_budget(candidate_steps,step_ms,overhead_ms,frequency_hz)` takes integer candidate_steps(K,),1<=K<=128, each1..10000; positive step_ms<=1e6, overhead_ms in [0,1e6], frequency_hz in [0.001,10000]. Return dict latency_ms:float64(K,) = overhead+steps*step_ms, feasible:bool(K,) for latency<=1000/frequency, and selected_steps:Python int equal largest feasible count, or0 if none. Preserve candidate order in arrays; duplicate counts permitted. This conservative contract requires a new plan every single control period.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original serving-budget exercise inspired by Diffusion Policy inference scheduling. A constant measured per-step cost is an explicit approximation, not a published timing guarantee.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
