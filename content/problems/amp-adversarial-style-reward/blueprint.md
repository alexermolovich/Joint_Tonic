---
{
  "schema_version": 1,
  "problem_id": "amp-adversarial-style-reward",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute an Adversarial Style Reward",
  "summary": "AMP uses a least-squares discriminator score, not a probability.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2021-adversarial-motion-priors",
    "policy-components"
  ],
  "paper_ids": [
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
  "entrypoint": "solution.adversarial_style_reward",
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
      "https://arxiv.org/abs/2104.02180"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2021-adversarial-motion-priors.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compute an Adversarial Style Reward

## Contract

`scores` is real `(B, T)`, with `1 <= B <= 128`, `1 <= T <= 256` and absolute values at most 100. `valid` is Boolean with the same shape.

Return a dictionary containing:

- `reward`: float64 `(B, T)`, equal to `max(0, 1 - 0.25*(score-1)**2)` at valid entries and zero elsewhere.
- `score_gradient`: float64 `(B, T)`, equal to `-0.5*(score-1)` only where the sample is valid and the unclipped reward is strictly positive; zero elsewhere. Choose zero at the clipping kinks, scores -1 and 3.
- `mean_reward`: Python float, the valid-sample mean, or zero if no sample is valid.

Scores are real least-squares discriminator outputs, not probabilities. Do not substitute a sigmoid or logarithmic GAN reward. This function does not train a discriminator or implement its gradient penalty.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
