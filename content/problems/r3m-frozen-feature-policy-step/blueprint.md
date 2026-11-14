---
{
  "schema_version": 1,
  "problem_id": "r3m-frozen-feature-policy-step",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Evaluate Frozen Features in a Small Policy",
  "summary": "A frozen encoder can still support learning a new robot controller.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2022-r3m",
    "policy-components"
  ],
  "paper_ids": [
    "2022-r3m"
  ],
  "paper_sections": [
    "Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim."
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
  "entrypoint": "solution.frozen_policy_step",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds."
    },
    "axes": "Video, frame, feature and policy-channel dimensions follow the typed contract",
    "timestamp_assumptions": "Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred.",
    "batching": "Video, frame, feature and policy-channel dimensions follow the typed contract"
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
    "authoring_notes": "Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.",
    "primary_urls": [
      "https://arxiv.org/html/2203.12601v3"
    ],
    "paper_card": "research/papers/robot-learning-rl/2022-r3m.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Evaluate Frozen Features in a Small Policy

## Contract

Features real(N,D), robot_state real(N,P), actions real(N,A), 1<=N<=4096,1<=D<=64,0<=P<=32,1<=A<=16; all finite abs<=10, actions normalized in[-1,1]. Train/evaluate bool(N,), disjoint, at least one train row; evaluation may be empty. Weight real(D+P,A), bias real(A,), abs<=10; learning_rate scalar[0,1]. All input features/state are already normalized dimensionless coordinates; action channels use the supplied normalized controller convention. Concatenate X=[features,state]. Initial predictions XW+b. Training loss mean squared error over train rows AND action channels. Gradient dW=2 Xtrain.T residual/(ntrain*A), db=2 sum(residual)/(ntrain*A). Compute simultaneous one-step SGD W'=W-lr*dW,b'=b-lr*db. Frozen features and all input arrays remain untouched. Return dict weight,bias,predictions (all N rows after update), train_loss_before,train_loss_after,evaluation_loss (same mean squared error on evaluation rows, NaN if none). Evaluation actions never affect the update. This is a single affine policy step on supplied frozen embeddings; the paper uses a BatchNorm-plus-MLP behavior-cloning policy and online success evaluation, neither reproduced here. No claim that action MSE equals task success.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
