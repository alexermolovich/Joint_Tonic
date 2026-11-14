---
{
  "schema_version": 1,
  "problem_id": "motion-task-reward-blend",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Combine Motion and Task Rewards",
  "summary": "A task score and a motion-quality score measure different properties.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2018-deepmimic",
    "policy-components"
  ],
  "paper_ids": [
    "2018-deepmimic",
    "2021-adversarial-motion-priors"
  ],
  "paper_sections": [
    "Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim."
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
  "entrypoint": "solution.combine_motion_rewards",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract."
    },
    "axes": "Batch, transition, joint and quaternion axes specified in the contract",
    "timestamp_assumptions": "Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents.",
    "batching": "Batch, transition, joint and quaternion axes specified in the contract"
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
    "authoring_notes": "Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.",
    "primary_urls": [
      "https://arxiv.org/abs/1804.02717"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2018-deepmimic.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Combine Motion and Task Rewards

## Contract

`motion_reward` and `task_reward` are real `(B, T)` arrays in `[0, 1]`, where `1 <= B <= 128` and `1 <= T <= 256`. `valid` is a Boolean array of the same shape. Each weight is a scalar in `[0, 100]`; weights need not sum to one.

Return a dictionary with `motion_contribution`, `task_contribution` and `reward`, each float64 `(B, T)`. Contributions equal the corresponding weight times the input, with exact zero at invalid samples. Reward is their sum. Also return `mean_reward`, a Python float equal to the global mean over valid samples, or zero when none exist.

The caller supplies either a DeepMimic imitation reward or an AMP style reward as the motion component; this function computes neither. Rewards use a common dimensionless convention at synchronized samples. Keep the two contributions visible: a combined reward is not a physical safety certificate.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
