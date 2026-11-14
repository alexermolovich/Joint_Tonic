---
schema_version: 1
paper_id: 2024-open-x-embodiment
title: 'Open X-Embodiment: Robotic Learning Datasets and RT-X Models'
authors:
  - Open X-Embodiment Collaboration (Abby O'Neill et al.)
year: 2024
venue_or_status: IEEE ICRA 2024
primary_url: 'https://arxiv.org/abs/2310.08864'
pdf_url: 'https://arxiv.org/pdf/2310.08864'
local_pdf: ./2024-open-x-embodiment.pdf
sha256: 13f16aff5afdee583dc25b3c570e9bb0cf6baefb59b539928d919588cd8d9246
bytes: 4011306
pages: 12
topics:
  - robot-data
  - cross-embodiment
  - dataset-mixtures
  - generalist-policies
  - transfer
modalities:
  - rgb
  - language
  - proprioception
  - actions
  - multi-robot-trajectories
track_role: core
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    The operational flow validates source episodes, constructs a weighted
    training mixture, and evaluates transfer on identified embodiments. These
    are data and evaluation stages, not a new universal action decoder.
  nodes:
    - id: stage-1
      title: Preserve episode semantics
      detail: >-
        Map observations and actions into explicit schema fields without
        dropping provenance.
      column: 0
      row: 0
      section: Preserve episode semantics
      problem_slugs:
        - validate-robot-episodes
        - map-shared-robot-episode
        - dataset-version-schema-drift
      planned_problems: []
    - id: stage-2
      title: Sample a training mixture
      detail: >-
        Choose source datasets deliberately rather than letting file counts
        determine training.
      column: 1
      row: 0
      section: Sample a training mixture
      problem_slugs:
        - balance-multidataset-batch
      planned_problems: []
    - id: stage-3
      title: Mask and evaluate transfer
      detail: >-
        Score supported action dimensions and report performance by embodiment
        and task.
      column: 2
      row: 0
      section: Mask and evaluate transfer
      problem_slugs:
        - mask-unavailable-action-dimensions
        - per-embodiment-transfer-matrix
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: validated episodes
    - from: stage-2
      to: stage-3
      label: mixture batches
---

## Core paper explanation

Open X-Embodiment brings robot datasets into a shared interface so policies can learn across embodiments, tasks, and collection sites. The difficult part is preserving meaning while standardizing representation: an action vector is incomplete without its units, coordinate frame, control mode, and timing. The RT-X experiments study transfer from such mixtures. A common schema helps make those experiments possible; it does not make different robots physically identical.

## Execution flow

The operational flow validates source episodes, constructs a weighted training mixture, and evaluates transfer on identified embodiments. These are data and evaluation stages, not a new universal action decoder.

### Preserve episode semantics

For episode $e$, represent time-aligned data as $\{(o_t,a_t,\tau_t)\}_{t=0}^{T_e-1}$ plus metadata $m_e$. Here $\tau_t$ is a timestamp in a declared clock and unit; $a_t\in\mathbb R^{D_e}$ has embodiment-specific channel meaning. A simple alignment diagnostic is

$$
\delta_t=|\tau_t^{\mathrm{camera}}-\tau_t^{\mathrm{state}}|.
$$

The acceptance tolerance is a dataset/control requirement, not a universal number from the paper. [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes) implements a bounded example of shape, value, frame, and timestamp checks. Reshaping an action array alone does not convert end-effector deltas into joint targets.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Runnable component: [Map Robot-Specific Data into a Shared Episode Schema](/problems/map-shared-robot-episode). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Detect Dataset-Version and Schema Drift](/problems/dataset-version-schema-drift). Implements the explicit bounded contract, not the complete source system.

### Sample a training mixture

Let dataset $D_i$ have nonnegative configured weight $w_i$, with at least one positive weight. A transparent mixture model is

$$
p(i)=\frac{w_i}{\sum_jw_j},\qquad x\sim D_i.
$$

These equations formalize a loader contract; they are not a claim that every RT-X run used one identical mixture. Sampling by episode versus transition changes the influence of long demonstrations. Record source identity, split, and sampling policy with every example. Train/test splits must respect shared scenes, operators, or episodes when those create leakage.


**Component practice**

- Runnable component: [Balance a Multi-Dataset Training Mixture](/problems/balance-multidataset-batch). Uses the bounded contract; no full paper reproduction is claimed.

### Mask and evaluate transfer

For a teaching batch with action availability mask $M_{bd}$, predicted action $\hat A$, and a chosen per-channel error $\ell$, use

$$
\mathcal L=\frac{\sum_{b,d}M_{bd}\,\ell(A_{bd},\hat A_{bd})}{\sum_{b,d}M_{bd}}.
$$

Require a nonzero denominator. Masking an unavailable channel excludes it from supervision; it does not establish that the remaining channels share units or control semantics. Report success per embodiment/task and compare with the relevant single-dataset baseline. An aggregate gain can hide a negative-transfer slice.


**Component practice**

- Runnable component: [Mask Unavailable Action Dimensions](/problems/mask-unavailable-action-dimensions). Implements the explicit bounded contract, not the complete source system.
- Runnable component: [Build a Per-Embodiment Transfer Matrix](/problems/per-embodiment-transfer-matrix). Implements the explicit bounded contract, not the complete source system.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).
- **Runnable component:** [Map Robot-Specific Data into a Shared Episode Schema](/problems/map-shared-robot-episode).
- **Runnable component:** [Balance a Multi-Dataset Training Mixture](/problems/balance-multidataset-batch).

**Component implementation map:**

- Runnable component: [Detect Dataset-Version and Schema Drift](/problems/dataset-version-schema-drift). Implements the explicit bounded contract, not the complete source system.
- Runnable component: [Mask Unavailable Action Dimensions](/problems/mask-unavailable-action-dimensions). Implements the explicit bounded contract, not the complete source system.
- Runnable component: [Build a Per-Embodiment Transfer Matrix](/problems/per-embodiment-transfer-matrix). Implements the explicit bounded contract, not the complete source system.

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Dataset diversity can improve transfer, but a common field name such as action can conceal incompatible physical contracts. Timing drift, duplicated episodes, gripper convention changes, and hidden source imbalance can all undermine generalization. Validate semantics before increasing dataset size.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2310.08864) · [Open-access manuscript](https://arxiv.org/pdf/2310.08864)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
