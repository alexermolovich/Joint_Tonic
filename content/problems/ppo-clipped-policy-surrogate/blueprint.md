---
{
  "schema_version": 1,
  "problem_id": "ppo-clipped-policy-surrogate",
  "content_version": "1.0.0",
  "status": "reviewed",
  "title": "Compute the Clipped Policy Surrogate",
  "summary": "PPO compares the new policy with the policy that collected each action.",
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
  "entrypoint": "solution.clipped_surrogate",
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

# Compute the Clipped Policy Surrogate

## Contract

Implement `clipped_surrogate(new_logp, old_logp, advantages, valid, epsilon)`. Each numeric input has shape (B,T), 1<=B<=64 and 1<=T<=1024. Log densities are in [-100,100], including positive continuous densities, and abs(new_logp-old_logp)<=40 at every entry. Advantages have magnitude <=1e6. valid is Boolean (B,T); epsilon is a scalar in [0,1]. Set ratio=exp(new-old), then take the minimum of ratio*advantage and clip(ratio,1-epsilon,1+epsilon)*advantage. Return a dict with terms:float64(B,T), exact zero at invalid slots; objective:Python float, the mean term over valid slots; loss:Python float, negative objective. With no valid slots all outputs are zero.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
