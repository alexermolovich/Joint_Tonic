---
{
  "schema_version": 1,
  "problem_id": "dreamer-imagined-latent-rollout",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Roll Out Imagined Latent Trajectories",
  "summary": "Start imagination from one known latent state and propagate using actions and learned dynamics only.",
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
  "entrypoint": "solution.imagine_latents",
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

# Roll Out Imagined Latent Trajectories

## Contract

initial_state real(B,D), actions real(B,H,A), state_weight real(D,D),action_weight real(A,D),bias/reward_weight/continue_weight real(D,),reward_bias/continue_bias scalar[-10,10];1<=B<=32,0<=H<=64,1<=D,A<=32; all array entries abs<=10. Supplied actions normalized dimensionless. Original deterministic surrogate h[t+1]=tanh(h[t]@state_weight+actions[t]@action_weight+bias); reward[t]=h[t+1]@reward_weight+reward_bias; continuation[t]=stable_sigmoid(h[t+1]@continue_weight+continue_bias). Return dict states float64(B,H+1,D) including initial, rewards float64(B,H), continuation float64(B,H). No posterior observations are available after initialization; no stopping or zeroing when continuation is low (it is a prediction for return weighting). This is a supplied deterministic tanh dynamics teaching block, NOT Dreamer's RSSM/categorical sampling, trained world model, actor optimization or complete robot simulation. Preserve inputs and support zero horizon.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
