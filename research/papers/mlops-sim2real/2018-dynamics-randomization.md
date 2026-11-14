---
schema_version: 1
paper_id: "2018-dynamics-randomization"
title: "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization"
authors:
  - "Xue Bin Peng"
  - "Marcin Andrychowicz"
  - "Wojciech Zaremba"
  - "Pieter Abbeel"
year: 2018
venue_or_status: "IEEE ICRA 2018"
primary_url: "https://arxiv.org/abs/1710.06537"
pdf_url: "https://arxiv.org/pdf/1710.06537"
local_pdf: "./2018-dynamics-randomization.pdf"
sha256: "a15cb24630a11218865027024ae2353f80f46d40371b42dccb2b24e9d00d62d8"
bytes: 2845918
pages: 8
topics:
  - "sim-to-real"
  - "dynamics-randomization"
  - "reinforcement-learning"
  - "robust-control"
  - "calibration"
modalities:
  - "robot-state"
  - "actions"
  - "rewards"
  - "dynamics-parameters"
  - "trajectories"
track_role: "core"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Use a simple control environment to teach training and evaluation across distributions of mass, friction, damping, delay, and calibration error. Make worst-slice behavior visible alongside average return.

## Contribution

The method trains a policy under randomized simulator dynamics so the policy adapts to parameters that differ from any single calibrated simulator, improving transfer to a physical robot without real-world policy training.

## Prerequisite concepts

- Markov decision processes and discounted return
- Basic feedback control or reinforcement learning
- Rigid-body parameters and actuator delay
- Robust statistics and seeded simulation

## Essential theory

Let \(\phi\) be dynamics parameters and \(\tau\) a trajectory induced by policy \(\pi_\theta\). The randomized objective is

$$
J(\theta)=\mathbb{E}_{\phi\sim p(\phi),\;\tau\sim p(\tau\mid\pi_\theta,\phi)}
\left[\sum_{t=0}^{T-1}\gamma^t r(s_t,a_t)\right].
$$

For deployment, also track a tail or worst-slice metric, for example

$$
J_{\mathrm{robust}}=\min_{b\in\mathcal{B}}\;\mathbb{E}[R(\tau)\mid \phi\in b],
$$

where \(\mathcal{B}\) partitions the allowed dynamics range.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Dynamics sampler | Parameter distributions and seed | Episode dynamics record | Samples are reproducible and physically valid | Implement bounded mass/friction/delay sampling |
| Environment wrapper | Base simulator and dynamics record | Parameterized transitions | The episode uses one traceable parameter realization | Implement delayed actuation or one randomized property |
| Robust evaluator | Returns and parameter bins | Mean, tail, and worst-bin metrics | Aggregate results retain parameter-slice provenance | Compute robust return summaries |

- Simulator with parameterized dynamics
- Training distribution over physical parameters and delays
- Policy optimization loop
- Nominal, randomized, and held-out evaluation suites
- Calibration-error and real-robot transfer tests

## Data and evaluation

Use a 1D/2D pushing or reaching environment. Evaluate mean return, success rate, tail performance, parameter-slice curves, and sensitivity outside the training range over fixed seed sets.

## Limitations and failure modes

Poorly chosen ranges can produce unstable or unrealistic simulations, and broad training can reduce nominal performance. Simulation still omits unmodeled effects, wear, contact complexity, and observation failures.

## Implementation decomposition

1. Parameterize mass, friction, gain, delay, and observation noise.
2. Sample dynamics from a versioned distribution per episode.
3. Train or evaluate a policy over fixed seed/parameter suites.
4. Aggregate mean, quantile, and worst-bin performance.
5. Select deployment ranges with explicit safety constraints.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Dynamics Parameter Sampler | Simulation utility | Easy | Distribution spec and seed | Parameter sets plus provenance | Bounds, determinism, invalid-parameter rejection |
| Delayed Actuator Wrapper | Control simulation | Medium | Action sequence and delay model | Applied actions by time step | Queue semantics, variable delay, reset behavior |
| Robust Return Aggregator | Evaluation | Medium | Returns and parameter bins | Mean, quantiles, worst-bin score | Correct grouping, empty bins, deterministic summaries |
| Safe Randomization Bounds | Optimization | Hard | Evaluation grid and constraints | Feasible bounds maximizing coverage | Constraint satisfaction, tie-breaking, held-out score |

## Visual teaching plan

- Interactive mass/friction/delay sliders with a live trajectory overlay.
- Heatmap of success across two dynamics parameters, showing train range and held-out region.
- Distribution plot comparing nominal-only and randomized policy returns.
- Timeline animation of commanded versus delayed/applied actions.

## MLOps and deployment extensions

Treat the dynamics distribution as a versioned artifact linked to simulator and controller versions. Validate sampled parameters for physical plausibility, maintain fixed robustness suites in CI, and require staged hardware tests before fleet rollout.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/1710.06537)
- [arXiv PDF](https://arxiv.org/pdf/1710.06537)

