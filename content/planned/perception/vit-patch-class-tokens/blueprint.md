---
schema_version: 1
problem_id: vit-patch-class-tokens
content_version: 0.1.0
status: reviewed
title: Build Learned Patch and Class Tokens
summary: Build Learned Patch and Class Tokens
type: function
difficulty: easy
estimated_minutes: 25
domains:
  - perception
topics:
  - vision-transformer
  - paper-component
paper_ids:
  - 2021-vision-transformer
paper_sections:
  - Mechanism and scope defined in theory.md
track_ids: []
prerequisite_problem_ids:
  - vit-patchify-reconstruct
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build
  dependencies:
    torch: 2.6.0+cpu
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
entrypoint: solution.build_vit_tokens
physical_contract:
  frames:
    - Declared explicitly in learner contract
  units:
    features: dimensionless; image indices in pixels where applicable
  axes: >-
    patches(B,N,F), projection(F,D), bias(D), cls(D), positions(N+1,D);
    result(B,N+1,D).
  timestamp_assumptions: Same upstream observation or training snapshot; no timestamp input.
  batching: >-
    patches(B,N,F), projection(F,D), bias(D), cls(D), positions(N+1,D);
    result(B,N+1,D).
grading:
  mode: numerical
  seed: 20261113
  rtol: 1.e-7
  atol: 1.e-9
  public_case_families:
    - worked-examples
    - minimal-shape
  hidden_case_families:
    - validation
    - empty-policy
    - noncontiguous
    - immutability
    - deterministic-order
    - realistic-batch
  performance_class: none
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: >-
    Original teaching contract and synthetic fixtures, no copied paper
    prose/figures/code.
  primary_urls:
    - 'https://arxiv.org/abs/2010.11929'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---

# Build Learned Patch and Class Tokens

## Contract

Implement build_vit_tokens(patches, projection, bias, cls, positions). All five arguments are finite CPU PyTorch tensors with the same dtype float32 or float64 and absolute values <=100. Require patches shape (B,N,F), projection (F,D), bias and cls (D,), positions (N+1,D). B may be zero; N,F,D are positive; the named dimensions B,N,F,D are each <=1024 (the positions sequence N+1 may be1025) and every input and output has at most 1,000,000 elements. Compute each patch row @ projection + bias, prepend the supplied learned cls vector to each batch item, then add positions to every batch. Return a new (B,N+1,D) tensor preserving dtype/device and gradient paths to all inputs. Do not alter inputs. No dropout, normalization, attention, image patchification, or parameter initialization. TypeError for non-tensors; ValueError for all other violations, including shapes, bounds, dtype/device. A zero batch returns (0,N+1,D). Feature and positional values are dimensionless; sequence order is caller-provided image-patch order, and all patches in a row belong to one exposure. This is the token-assembly step of ViT, not a trained encoder.

## Plan and proof

Implement only the typed component above. Independent review precedes publication. Validate both worked examples, documented errors and boundaries, stable layout/order, input preservation and realistic batches. Use actual isolated Run/Submit checks; no performance leaderboard. Source is the paired paper card and primary URL. Original theory contains defined mathematics and a static trace-table visual with text equivalent. Runtime image digest is pending; actual local worker caps are declared.
