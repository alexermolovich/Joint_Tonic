---
schema_version: 1
paper_id: "2017-domain-randomization"
title: "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
authors:
  - "Josh Tobin"
  - "Rachel Fong"
  - "Alex Ray"
  - "Jonas Schneider"
  - "Wojciech Zaremba"
  - "Pieter Abbeel"
year: 2017
venue_or_status: "IEEE/RSJ IROS 2017"
primary_url: "https://arxiv.org/abs/1703.06907"
pdf_url: "https://arxiv.org/pdf/1703.06907"
local_pdf: "./2017-domain-randomization.pdf"
sha256: "3fc98c5f4cea050686d45858e647e1b704492121fdae80f8fcd5d560c107f11f"
bytes: 4066798
pages: 8
topics:
  - "sim-to-real"
  - "domain-randomization"
  - "synthetic-data"
  - "perception"
  - "robustness"
modalities:
  - "synthetic-rgb"
  - "real-rgb"
  - "object-pose"
  - "simulator-parameters"
track_role: "core"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Sample rendering parameters, generate labeled images, and evaluate transfer on held-out variations and real observations.","nodes":[{"id":"stage-1","title":"Sample appearance parameters","detail":"Choose a reproducible distribution over simulator visual factors.","column":0,"row":0,"section":"Sample appearance parameters","problem_slugs":[],"planned_problems":["Build a Seeded Visual Randomization Sampler","Stratify Texture, Lighting, Camera, and Distractor Factors","Version a Simulation Scenario Distribution"]},{"id":"stage-2","title":"Train across variation","detail":"Optimize task predictions over the sampled appearance distribution.","column":1,"row":0,"section":"Train across variation","problem_slugs":[],"planned_problems":["Average Per-Scenario Perception Losses"]},{"id":"stage-3","title":"Measure transfer and coverage","detail":"Report behavior across factor ranges rather than only a pooled average.","column":2,"row":0,"section":"Measure transfer and coverage","problem_slugs":[],"planned_problems":["Measure Performance Across Shift Buckets","Estimate Scenario Coverage and Confidence Intervals"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"randomized images"},{"from":"stage-2","to":"stage-3","label":"trained perception model"}]}
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

- Build a Seeded Visual Randomization Sampler — unreviewed idea; contract and evaluator required.
- Stratify Texture, Lighting, Camera, and Distractor Factors — unreviewed idea; contract and evaluator required.
- Version a Simulation Scenario Distribution — unreviewed idea; contract and evaluator required.


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

- Measure Performance Across Shift Buckets — unreviewed idea; contract and evaluator required.
- Estimate Scenario Coverage and Confidence Intervals — unreviewed idea; contract and evaluator required.


## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Build a Seeded Visual Randomization Sampler — unreviewed idea; contract and evaluator required.
- Stratify Texture, Lighting, Camera, and Distractor Factors — unreviewed idea; contract and evaluator required.
- Version a Simulation Scenario Distribution — unreviewed idea; contract and evaluator required.
- Average Per-Scenario Perception Losses — unreviewed idea; contract and evaluator required.
- Measure Performance Across Shift Buckets — unreviewed idea; contract and evaluator required.
- Estimate Scenario Coverage and Confidence Intervals — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Appearance variation can reduce reliance on synthetic textures, but it does not solve incorrect geometry, sensor timing, or dynamics. Camera blur, specular materials, and calibration changes may sit outside the randomization family. Track transfer failures by their physical cause.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1703.06907) · [Open-access manuscript](https://arxiv.org/pdf/1703.06907)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
