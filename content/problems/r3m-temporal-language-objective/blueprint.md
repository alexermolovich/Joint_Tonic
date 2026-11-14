---
{
  "schema_version": 1,
  "problem_id": "r3m-temporal-language-objective",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Combine Temporal and Language Alignment Losses",
  "summary": "Nearby visual states, meaningful language progress and compact features provide different learning signals.",
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
  "entrypoint": "solution.representation_objective",
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

# Combine Temporal and Language Alignment Losses

## Contract

Embeddings real (B,4,D), 0<=B<=512, 1<=D<=256, absolute values<=100. Slots are anchor i, nearby j, farther k, and other-video anchor; ordering and video identity have already been validated. Language logits real(B,3), absolute values<=1000, ordered positive later/correct-language, earlier/correct-language, other-video/correct-language. These are supplied scores from a learned progress model, not image-caption cosine similarities. Valid bool(B,), weights real(4,) in[0,100]. Compute temporal logits [-norm(zi-zj), -norm(zi-zk), -norm(zi-zother)] using Euclidean norm, then negative log-softmax at index0. Language term is negative log-softmax(language_logits) at index0. L1 and L2 terms are respectively sum(abs(zi)) and sqrt(sum(zi**2)) for anchor embedding, NOT squared L2. Return dict per_example float64(B,4) (invalid rows zero), components float64(4,) (mean over valid rows, or zeros when none), loss Python float dot(weights,components). Averaging convention and anchor-only regularization are explicitly pinned; the paper's batch-summed objective differs only in the declared reduction/weight scale. No gradients or model training requested. Every input including invalid rows is still validated.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
