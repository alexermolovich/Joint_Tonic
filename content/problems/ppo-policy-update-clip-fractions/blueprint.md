---
{
  "schema_version": 1,
  "problem_id": "ppo-policy-update-clip-fractions",
  "content_version": "1.0.0",
  "status": "reviewed",
  "title": "Report Policy Update Clip Fractions",
  "summary": "A probability ratio outside the clipping interval does not always change PPO\u2019s objective.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2017-proximal-policy-optimization",
    "policy-components"
  ],
  "paper_ids": [
    "2017-proximal-policy-optimization"
  ],
  "paper_sections": [
    "Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy."
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
  "entrypoint": "solution.policy_clip_metrics",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units."
    },
    "axes": "B rollout streams, T samples; scalar reductions only over Boolean-valid entries",
    "timestamp_assumptions": "Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits.",
    "batching": "B rollout streams, T samples; scalar reductions only over Boolean-valid entries"
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
    "authoring_notes": "Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.",
    "primary_urls": [
      "https://arxiv.org/abs/1707.06347"
    ],
    "paper_card": "research/papers/robot-learning-rl/2017-proximal-policy-optimization.md",
    "manifest": "research/IMPLEMENTATION_BACKLOG.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Report Policy Update Clip Fractions

## Contract

Implement `policy_clip_metrics(new_logp, old_logp, advantages, valid, epsilon)`. Numeric arrays are real (B,T), 1<=B<=64, 1<=T<=1024; validity is Boolean with the same shape. Log densities lie in [-100,100] and abs(new-old)<=40; epsilon is in [0,1]. Return a dict count:Python int, ratio_clip_fraction:Python float for valid ratios strictly outside [1-epsilon,1+epsilon], active_clip_fraction:Python float for valid entries where (advantage>0 and ratio>1+epsilon) or (advantage<0 and ratio<1-epsilon), and approx_kl:Python float equal to valid mean(exp(delta)-1-delta), delta=new-old. Each numeric result is zero when count=0. Zero advantages never activate objective clipping. Preserve the strict endpoint convention.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
