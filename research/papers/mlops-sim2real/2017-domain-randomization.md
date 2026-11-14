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
---

## Agent brief

Implement a seeded visual-domain randomizer and evaluate performance by randomization factor and shift bucket. The goal is to reason about coverage and transfer, not merely generate colorful images.

## Contribution

The paper shows that broad randomization of simulated visual factors can make a real scene appear like another training variation, enabling a perception model trained only in simulation to support real-world manipulation.

## Prerequisite concepts

- Supervised learning and object localization
- Camera and rendering parameters
- Random variables and experimental controls
- Train/test distribution shift

## Essential theory

Let \(\phi\) denote simulator appearance parameters such as texture, lighting, camera pose, and clutter. Domain-randomized training minimizes an expected loss over a parameter distribution:

$$
\min_\theta\;\mathbb{E}_{\phi\sim p(\phi)}\;\mathbb{E}_{(x,y)\sim \mathrm{Sim}(\phi)}
[\ell(f_\theta(x),y)].
$$

The practical design problem is choosing \(p(\phi)\) wide enough to cover relevant real conditions without making learning needlessly hard.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Parameter sampler | Distribution spec and seed | Appearance parameter record | Samples are reproducible and inside declared bounds | Implement one seeded distribution family |
| Synthetic generator | Scene plus sampled parameters | Labeled image and provenance | Labels and sampled parameters stay aligned | Render or synthesize one factorized scene |
| Shift evaluator | Predictions, labels, factor metadata | Overall and sliced metrics | Every sample belongs to declared evaluation slices | Compute one per-factor robustness report |

- Simulator scene and labeled target pose
- Distributions over textures, lights, camera, clutter, and object appearance
- Synthetic dataset generator with recorded seeds/parameters
- Perception model and localization metric
- Real-image transfer evaluation and factor ablations

## Data and evaluation

Use a lightweight procedural 2D renderer or supplied synthetic features. Hold out factor combinations and a real-like target domain. Report localization error, success under a distance threshold, and per-factor robustness.

## Limitations and failure modes

Randomization cannot cover every real artifact, and implausible samples may waste capacity. Success depends on the task, simulator labels, chosen ranges, and whether the randomized variables include the real failure modes.

## Implementation decomposition

1. Define typed parameter distributions and safe ranges.
2. Generate deterministic scenes from a master seed.
3. Store every sampled parameter with the label.
4. Stratify evaluation by individual and combined shifts.
5. Tune ranges using coverage reports rather than test leakage.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Seeded Scene Randomizer | Simulation utility | Medium | Distribution spec, seed, sample count | Parameter records or rendered scenes | Determinism, bounds, independence/declared coupling |
| Stratified Randomization Plan | Sampling | Medium | Factor levels and budget | Balanced factor combinations | Coverage, budget, reproducible allocation |
| Sim-to-Real Shift Report | Evaluation | Hard | Predictions, labels, factor metadata | Overall and per-shift metrics | Correct slices, confidence intervals, missing-slice handling |
| Range Coverage Checker | Validation | Easy | Sampled values and allowed ranges | Coverage gaps and violations | Exact bounds, quantile summaries, clear evidence |

## Visual teaching plan

- Grid of one base scene with one factor changed at a time.
- Interactive sliders for texture, light, camera, and clutter ranges with live coverage histograms.
- Parallel-coordinates plot linking sampled parameters to localization error.
- Train-distribution cloud versus real-condition point in a simplified 2D parameter space.

## MLOps and deployment extensions

Version the simulator, assets, renderer, parameter distribution, and seed manifest. Monitor real fleet conditions against training coverage and trigger new simulation generation when cameras, sites, or lighting move outside supported ranges.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/1703.06907)
- [arXiv PDF](https://arxiv.org/pdf/1703.06907)

