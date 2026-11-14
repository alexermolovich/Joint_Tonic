---
{
  "schema_version": 1,
  "problem_id": "dreamer-balanced-latent-loss",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Compute a Balanced Latent-Model Loss",
  "summary": "The dynamics prior should learn to predict the posterior, while the posterior should become easier to predict without discarding useful information.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-dreamerv3",
    "policy-components"
  ],
  "paper_ids": [
    "2023-dreamerv3"
  ],
  "paper_sections": [
    "A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark."
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
  "entrypoint": "solution.balanced_latent_loss",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats."
    },
    "axes": "Batch, categorical-group, category, rollout-time and latent axes are defined in the contract",
    "timestamp_assumptions": "Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion.",
    "batching": "Batch, categorical-group, category, rollout-time and latent axes are defined in the contract"
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
    "authoring_notes": "A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.",
    "primary_urls": [
      "https://arxiv.org/html/2301.04104v2"
    ],
    "paper_card": "research/papers/robot-learning-rl/2023-dreamerv3.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Compute a Balanced Latent-Model Loss

## Contract

posterior_logits and prior_logits real (B,G,C), 1<=B<=128, 1<=G<=32, 2<=C<=32, abs<=50; prediction_loss real (B,) in [0,1e6], valid Boolean (B,). Each group is an independent categorical latent variable. Compute softmax s_q,s_p, then q=.99*s_q+.01/C, p=.99*s_p+.01/C. Per row K=sum over G,C q*(log(q)-log(p)), in nats. Dynamics loss max(1,KL(stop(q)||p)); representation loss max(1,KL(q||stop(p))); their forward values equal max(1,K), but gradient paths differ. Return dict kl float64(B) K valid else NaN; loss Python float mean over valid rows of prediction_loss+1.1*max(1,K) (0 if none); prior_gradient and posterior_gradient float64(B,G,C) analytical gradients with respect to input logits, using coefficient 1 on dynamics prior path and coefficient 0.1 on representation posterior path; prediction_gradient float64(B) 1/N valid else 0. At K<=1 both KL gradients exactly0 (explicit kink convention). Invalid rows have zero gradients and do not enter normalization. Include derivative of .99 softmax+.01/C. This implements the paper's specified loss balancing/free-nat/uniform-mixture component with supplied prediction losses, not the complete recurrent world model or straight-through latent sampling.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
