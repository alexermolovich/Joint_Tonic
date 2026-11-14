---
schema_version: 1
problem_id: nerf-render-color-depth
content_version: 0.1.0
status: reviewed
title: Render Color and Expected Depth Along a Ray
summary: Render Color and Expected Depth Along a Ray
type: function
difficulty: medium
estimated_minutes: 30
domains:
  - perception
topics:
  - nerf
  - paper-component
paper_ids:
  - 2020-nerf
paper_sections:
  - Mechanism and limits stated in theory.md
track_ids: []
prerequisite_problem_ids:
  - nerf-alpha-compositing
runtime:
  language: python
  python: 3.12.3
  image_digest: null
  image_status: pending-image-build
  dependencies:
    numpy: 2.2.4
  limits:
    wall_seconds: 18
    cpu_seconds: 10
    memory_mb: 4096
    output_kb: 64
entrypoint: solution.render_rays
physical_contract:
  frames:
    - Contract declares observation and coordinate assumptions
  units:
    features: dimensionless; ray distances in meters where applicable
  axes: >-
    weights(R,S),colors(R,S,3),depths(R,S),background(R,),background_rgb(3,);
    return rgb(R,3), depth(R), valid(R).
  timestamp_assumptions: One synchronized upstream observation or training snapshot.
  batching: >-
    weights(R,S),colors(R,S,3),depths(R,S),background(R,),background_rgb(3,);
    return rgb(R,3), depth(R), valid(R).
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
    - numerical-boundaries
    - independent-oracle
  performance_class: none
fixtures:
  source: original-synthetic
  license: CC0-1.0
  version_or_hash: synthetic-v1-seed-20261113
provenance:
  authoring_notes: Original scoped exercise; no paper figure/prose/code copied.
  primary_urls:
    - 'https://arxiv.org/abs/2003.08934'
  implementation_urls: []
owners:
  - perception_implementation
reviewers:
  - vla_implementation
---

# Render Color and Expected Depth Along a Ray

## Contract

Implement render_rays(weights, colors, depths, background, background_rgb). All inputs are finite NumPy float64 arrays with shapes (R,S),(R,S,3),(R,S),(R,),(3,), R,S>=1, each dimension<=1024 and colors at most1,000,000 elements. Weights/background lie in [0,1]; require weights.sum(1)+background close to1 with atol1e-6,rtol0. Colors and background_rgb lie in [0,1] as linear RGB. Depths lie in [0,1e6] meters along normalized rays, nondecreasing per row. Compute rgb=sum(weights[...,None]*colors,axis=1)+background[:,None]*background_rgb. Return conditional foreground depth sum(weights*depths)/sum(weights) only where foreground mass>1e-8; elsewhere depth=NaN and valid=False. Return new float64 rgb/depth and bool valid, preserving inputs. TypeError for non-arrays, ValueError for all other violations. No clipping or renormalizing supplied compositing weights; depth normalization is intentionally conditional on a foreground hit. No gamma conversion, density evaluation, background depth assignment, or scene training.

## Plan and verification

Review source fidelity, mathematics, numerical examples and edge/error behavior before implementation. Implement original starter/reference/public+hidden tests. Confirm actual isolated Run and Submit, and a starter negative control. Use static numerical/shape traces with text alternatives and original theory. Record only actual local worker caps; an OCI image digest remains pending. No dataset or full-paper reproduction is implied.
