---
schema_version: 1
paper_id: "2021-ikflow"
title: "IKFlow: Generating Diverse Inverse Kinematics Solutions"
authors: ["Ames, Barrett","Morgan, Jeremy","Konidaris, George"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2111.08933"
pdf_url: "https://arxiv.org/pdf/2111.08933"
local_pdf: "./2021-ikflow.pdf"
sha256: "8b1b41b7321275ad9039fc02b7e41c65e45365ee540ad722f971481eb1a95995"
bytes: 5312937
pages: 8
topics: ["planning-control-ik","ikflow"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Condition an invertible model","detail":"Learn joint configurations associated with target poses.","column":0,"row":0,"section":"Condition an invertible model","problem_slugs":[],"planned_problems":["Encode a Target Pose for Conditional IK"]},{"id":"stage-2","title":"Train by change of variables","detail":"Account for the flow Jacobian in likelihood.","column":1,"row":0,"section":"Train by change of variables","problem_slugs":[],"planned_problems":["Compute a Conditional Flow Log-Likelihood"]},{"id":"stage-3","title":"Sample and verify IK","detail":"Generate multiple candidates, refine, and reject invalid ones.","column":2,"row":0,"section":"Sample and verify IK","problem_slugs":[],"planned_problems":["Measure End-Effector Pose Error","Filter Sampled IK Configurations by Joint Limits","Cluster Diverse IK Solutions"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"pose-conditioned samples"},{"from":"stage-2","to":"stage-3","label":"latent samples"}]}
---

## Core paper explanation

IKFlow learns a conditional distribution of inverse-kinematics solutions rather than returning only one configuration. A normalizing flow produces diverse approximate solutions for a desired end-effector pose, which can then be refined and checked.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Condition an invertible model

For pose condition $y$ and appropriately dimensioned latent $z$, a conditional invertible map gives $q=f_\theta(z;y)$. Training uses joint samples with targets computed by forward kinematics. The actual model uses its specified augmentation/noise scheme to make the density-learning problem tractable.


**Component practice**

- Encode a Target Pose for Conditional IK — unreviewed idea; contract and evaluator required.

### Train by change of variables

In matching dimensions, the density relation is
$$\log p(q\mid y)=\log p(z)-\log\left|\det\frac{\partial f_\theta(z;y)}{\partial z}\right|.$$
This explains the normalizing-flow mechanism; padding and augmentation must follow the actual architecture. A deterministic one-to-one pose-to-joint regressor cannot represent all redundant solutions.


**Component practice**

- Compute a Conditional Flow Log-Likelihood — unreviewed idea; contract and evaluator required.

### Sample and verify IK

Check position error $e_p=\|p(q)-p^*\|_2$ in meters and orientation error $e_R=\|\operatorname{Log}(R^{*\top}R(q))\|_2$ in radians. Apply joint limits and collision checks separately. Low pose error does not imply collision-free reachability from the current configuration.


**Component practice**

- Measure End-Effector Pose Error — unreviewed idea; contract and evaluator required.
- Filter Sampled IK Configurations by Joint Limits — unreviewed idea; contract and evaluator required.
- Cluster Diverse IK Solutions — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Encode a Target Pose for Conditional IK — unreviewed idea; contract and evaluator required.
- Compute a Conditional Flow Log-Likelihood — unreviewed idea; contract and evaluator required.
- Measure End-Effector Pose Error — unreviewed idea; contract and evaluator required.
- Filter Sampled IK Configurations by Joint Limits — unreviewed idea; contract and evaluator required.
- Cluster Diverse IK Solutions — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Diverse IK candidates help choose configurations with useful clearance or manipulability. Learned samples are approximate; calibration errors and unseen poses require explicit residual checks and fallback behavior.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2111.08933) · [Open-access manuscript](https://arxiv.org/pdf/2111.08933)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
