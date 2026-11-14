---
{
  "schema_version": 1,
  "problem_id": "r3m-time-contrastive-video-triplets",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Sample Time-Contrastive Video Triplets",
  "summary": "Temporal supervision depends on which frames are compared.",
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
  "entrypoint": "solution.sample_video_triplets",
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

# Sample Time-Contrastive Video Triplets

## Contract

Lengths integer (V,), 2<=V<=1024, each 1..100000; implicit video IDs are row indices. At least one video has length >=3. Uniforms real (B,6), 0<=B<=16384, every entry in [0,1). At each batch row: draw the anchor video uniformly from the sorted IDs with length>=3 using column 0; draw i=floor(u1*(L-2)); j=i+1+floor(u2*(L-i-2)); k=j+1+floor(u3*(L-j-1)); draw a different video from sorted remaining IDs with column 4; draw its frame floor(u5*other_length). Return dict video_ids int64(B,), frames int64(B,3), negative_video_ids int64(B,), negative_frames int64(B,). Output obeys i<j<k and negative video != anchor video. Frame indices are zero-based ordinal positions; no constant frame-rate or seconds implied. This is an explicit replayable sequential sampling recipe, NOT a uniform distribution over all possible triples or a claim to match the paper's random sampler exactly.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
