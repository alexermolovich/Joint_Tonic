---
schema_version: 1
paper_id: 2017-domain-randomization
title: >-
  Domain Randomization for Transferring Deep Neural Networks from Simulation to
  the Real World
authors:
  - Josh Tobin
  - Rachel Fong
  - Alex Ray
  - Jonas Schneider
  - Wojciech Zaremba
  - Pieter Abbeel
year: 2017
venue_or_status: IEEE/RSJ IROS 2017
primary_url: 'https://arxiv.org/abs/1703.06907'
pdf_url: 'https://arxiv.org/pdf/1703.06907'
local_pdf: ./2017-domain-randomization.pdf
sha256: 3fc98c5f4cea050686d45858e647e1b704492121fdae80f8fcd5d560c107f11f
bytes: 4066798
pages: 8
topics:
  - sim-to-real
  - domain-randomization
  - synthetic-data
  - perception
  - robustness
modalities:
  - synthetic-rgb
  - real-rgb
  - object-pose
  - simulator-parameters
track_role: core
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Sample rendering parameters, generate labeled images, and evaluate transfer
    on held-out variations and real observations.
  nodes:
    - id: stage-1
      title: Sample appearance parameters
      detail: Choose a reproducible distribution over simulator visual factors.
      column: 0
      row: 0
      section: Sample appearance parameters
      problem_slugs:
        - seeded-visual-randomization
        - stratify-visual-factors
        - version-simulation-distribution
      planned_problems: []
    - id: stage-2
      title: Train across variation
      detail: Optimize task predictions over the sampled appearance distribution.
      column: 1
      row: 0
      section: Train across variation
      problem_slugs: []
      planned_problems:
        - Average Per-Scenario Perception Losses
    - id: stage-3
      title: Measure transfer and coverage
      detail: Report behavior across factor ranges rather than only a pooled average.
      column: 2
      row: 0
      section: Measure transfer and coverage
      problem_slugs:
        - shift-bucket-performance
        - scenario-coverage-confidence
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: randomized images
    - from: stage-2
      to: stage-3
      label: trained perception model
---

## Core paper explanation

Visual domain randomization varies simulator appearance so a perception model cannot rely on one narrow synthetic rendering style. Lighting, textures, object appearance, and camera-related nuisance factors are sampled during training. The goal is to learn useful task structure across that variation, making real images less exceptional than they would be under one fixed simulator appearance.

## Execution flow

Sample rendering parameters, generate labeled images, and evaluate transfer on held-out variations and real observations.

### Sample appearance parameters

Let $\xi$ contain lighting, texture, and other declared rendering parameters. Sample

$$
\xi\sim p_{\mathrm{train}}(\xi),\qquad I=\operatorname{Render}(s,\xi).
$$

The scene state $s$ determines task labels. Randomization must not silently change the label’s physical meaning. Seed every random source and record sampled parameters so a failure can be replayed.


**Component practice**

- Runnable component: [Build a Seeded Visual Randomization Sampler](/problems/seeded-visual-randomization). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Stratify Texture, Lighting, Camera, and Distractor Factors](/problems/stratify-visual-factors). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Version a Simulation Scenario Distribution](/problems/version-simulation-distribution). Implements the bounded learning contract linked here, not the complete paper.


### Train across variation

For label $y(s)$ and model $f_\theta$, an expected-risk description is

$$
\min_\theta\mathbb E_{s,\xi}\,\ell(f_\theta(\operatorname{Render}(s,\xi)),y(s)).
$$

Broadening a distribution is not automatically beneficial: randomization that destroys task evidence or creates impossible images can harm learning. Distinguish factors that vary appearance from factors that change the task itself.


**Component practice**

- Average Per-Scenario Perception Losses — unreviewed idea; contract and evaluator required.


### Measure transfer and coverage

For evaluation bucket $b$, report risk $R_b=\mathbb E[\ell\mid\xi\in b]$ and sample count. A simple coverage diagnostic is

$$
\mathrm{coverage}=\frac{\#\{b:n_b>0\}}{\#\{b\}}.
$$

This is a teaching diagnostic, not a transfer guarantee. Held-out real images remain necessary because the simulator’s parameter family may omit important real effects.


**Component practice**

- Runnable component: [Measure Performance Across Shift Buckets](/problems/shift-bucket-performance). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Estimate Scenario Coverage and Confidence Intervals](/problems/scenario-coverage-confidence). Implements the bounded learning contract linked here, not the complete paper.


## Implement the components

Execution-flow nodes link runnable component exercises. Any additional research ideas remain explicitly labeled as future work and do not imply a complete paper reproduction.


**Component implementation map:**

- Runnable component: [Build a Seeded Visual Randomization Sampler](/problems/seeded-visual-randomization). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Stratify Texture, Lighting, Camera, and Distractor Factors](/problems/stratify-visual-factors). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Version a Simulation Scenario Distribution](/problems/version-simulation-distribution). Implements the bounded learning contract linked here, not the complete paper.
- Average Per-Scenario Perception Losses — unreviewed idea; contract and evaluator required.
- Runnable component: [Measure Performance Across Shift Buckets](/problems/shift-bucket-performance). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Estimate Scenario Coverage and Confidence Intervals](/problems/scenario-coverage-confidence). Implements the bounded learning contract linked here, not the complete paper.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Appearance variation can reduce reliance on synthetic textures, but it does not solve incorrect geometry, sensor timing, or dynamics. Camera blur, specular materials, and calibration changes may sit outside the randomization family. Track transfer failures by their physical cause.

## Scope of the runnable engineering components

The runnable follow-up components are original engineering extensions. [Seeded visual scenarios](/problems/seeded-visual-randomization) maps four fixed random columns into declared texture, exposure, yaw and distractor ranges. [Stratified factors](/problems/stratify-visual-factors) guarantees marginal strata, not exhaustive joint-factor coverage. [Shift metrics](/problems/shift-bucket-performance) retains missing buckets as unknown. [Coverage and Wilson intervals](/problems/scenario-coverage-confidence) assumes independent Bernoulli scenario trials and reports marginal uncertainty, not a simultaneous transfer guarantee. [Distribution versioning](/problems/version-simulation-distribution) binds units, reset policy and asset identity into canonical configuration evidence; these rules are not claimed as the paper's original experimental protocol.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1703.06907) · [Open-access manuscript](https://arxiv.org/pdf/1703.06907)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
