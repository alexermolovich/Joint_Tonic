---
{
  "schema_version": 1,
  "problem_id": "perturbed-linear-rollouts",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Roll Out Perturbed Control Sequences",
  "summary": "Roll out a batch of supplied control perturbations through a bounded discrete linear robot model.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "planning-control"
  ],
  "topics": [
    "planning-control",
    "path-integral-mpc"
  ],
  "paper_ids": [
    "2015-path-integral-mpc"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2015-path-integral-mpc"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.rollout_controls",
  "physical_contract": {
    "frames": [
      "Declared joint coordinates or a common right-handed world frame, as specified"
    ],
    "units": {
      "values": "Radians, seconds, meters and corresponding derivatives; normalized spaces explicitly identified"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent numerical mechanism",
      "Boundary and malformed inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "955fa83d0ce0f850dd4262144f94d4f22eab55e9d6c8d143268584e25d9cb7b2"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1509.01149"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Roll Out Perturbed Control Sequences

Implement `rollout_controls(initial, transition, control_map, nominal, perturbations)`.

Roll out a batch of supplied control perturbations through a bounded discrete linear robot model.

`initial` is float64 `(D,)`, `transition` `(D,D)`, `control_map` `(D,U)`, `nominal` `(H,U)`, `perturbations` `(K,H,U)`, with `1<=D,U<=8`, `1<=H<=64`, `1<=K<=128`. State and control coordinates are normalized dimensionless features in a fixed caller-defined order. The matrices describe one fixed controller period already discretized by the caller; do not apply another timestep. Require the maximum absolute row sum of transition to be at most 1; absolute control_map entries at most 10; absolute initial, nominal and perturbation entries at most 100.

Return fresh float64 `controls (K,H,U)=nominal+perturbations` and `states (K,H+1,D)` in a dictionary. Every rollout starts from initial. For each k,t, compute `states[k,t+1]=transition@states[k,t]+control_map@controls[k,t]`. Do not clip commands or state, sample new noise, compute costs or alter the supplied perturbations. This original bounded linear teaching model illustrates MPPI rollout structure; it does not model the full nonlinear stochastic dynamics or importance-sampling correction of the paper.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Scalar A=B=1, initial `[0.]`, nominal `[[1.],[2.]]`, one zero perturbation sequence yield controls `[[[1.],[2.]]]` and states `[[[0.],[1.],[3.]]]`.
2. The same inputs with perturbation sequence `[[[1.],[-1.]]]` yield controls `[[[2.],[1.]]]` and states `[[[0.],[2.],[3.]]]`.

## Source and scope

[Primary source](https://arxiv.org/abs/1509.01149). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Add the supplied perturbations to nominal controls once. Allocate all states, initialize every candidate independently, and advance across time while vectorizing candidates. O(KH(D²+DU)) time and O(KH(D+U)) output memory.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
