---
schema_version: 1
paper_id: "2023-maniskill-2"
title: "ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills"
authors: ["Gu, Jiayuan","Xiang, Fanbo","Li, Xuanlin","Ling, Zhan","Liu, Xiqiang","Mu, Tongzhou","Tang, Yihe","Tao, Stone","Wei, Xinyue","Yao, Yunchao","Yuan, Xiaodi","Xie, Pengwei","Huang, Zhiao","Chen, Rui","Su, Hao"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2302.04659"
pdf_url: "https://arxiv.org/pdf/2302.04659"
local_pdf: "./2023-maniskill-2.pdf"
sha256: "89fb794345d860ee696ca2f4d7a75059b15352b615794eeadb0e6075426136f0"
bytes: 7635048
pages: 30
topics: ["simulation-sim2real","maniskill-2"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Choose task and controller","detail":"Specify embodiment, object dynamics, and action semantics.","column":0,"row":0,"section":"Choose task and controller","problem_slugs":[],"planned_problems":["Validate a Robot-Controller-Task Configuration"]},{"id":"stage-2","title":"Collect visual experience","detail":"Use RGB-D or point clouds and versioned demonstrations.","column":1,"row":0,"section":"Collect visual experience","problem_slugs":["validate-robot-episodes","se3-transform-points"],"planned_problems":["Build a Vectorized Manipulation Batch"]},{"id":"stage-3","title":"Evaluate object and task generalization","detail":"Keep geometry splits and physical success checks explicit.","column":2,"row":0,"section":"Evaluate object and task generalization","problem_slugs":[],"planned_problems":["Validate Task-Specific Success Predicates","Report Generalization by Object Split"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"environment transitions"},{"from":"stage-2","to":"stage-3","label":"policy rollouts"}]}
---

## Core paper explanation

ManiSkill2 expands manipulation benchmarks across rigid and soft objects, mobile and stationary robots, and multiple observation/controller interfaces. A unified interface supports learning and classical planning while retaining task-specific physical contracts.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Choose task and controller

An action $a_t$ can represent joint targets, velocities, or end-effector commands depending on the controller. A conversion $u_t=C(a_t,s_t)$ maps policy output to actuator input. Matching tensor dimensions does not imply matching controllers.


**Component practice**

- Validate a Robot-Controller-Task Configuration — unreviewed idea; contract and evaluator required.

### Collect visual experience

A trajectory stores $(o_t,a_t,r_t,\mathrm{terminal}_t)$ with simulator state needed for reproduction. Rendering throughput and physics stepping can have different bottlenecks; record observation resolution, process count, and hardware when comparing sample rates.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Build a Vectorized Manipulation Batch — unreviewed idea; contract and evaluator required.

### Evaluate object and task generalization

For held-out object set $\mathcal O$, a teaching object-balanced score is $|\mathcal O|^{-1}\sum_{o\in\mathcal O}\hat p_o$. State whether the actual benchmark uses this or another aggregation. Soft-body tasks need deformation-aware goals; rigid-pose error alone cannot score them correctly.


**Component practice**

- Validate Task-Specific Success Predicates — unreviewed idea; contract and evaluator required.
- Report Generalization by Object Split — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).
- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).

**Planned component problems:**

- Validate a Robot-Controller-Task Configuration — unreviewed idea; contract and evaluator required.
- Build a Vectorized Manipulation Batch — unreviewed idea; contract and evaluator required.
- Validate Task-Specific Success Predicates — unreviewed idea; contract and evaluator required.
- Report Generalization by Object Split — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

A common benchmark interface broadens algorithm comparison. Different controllers, object solvers, and observation privilege can still make nominally similar experiments incomparable unless configurations are recorded.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2302.04659) · [Open-access manuscript](https://arxiv.org/pdf/2302.04659)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
