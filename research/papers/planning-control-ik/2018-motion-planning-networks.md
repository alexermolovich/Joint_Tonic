---
schema_version: 1
paper_id: "2018-motion-planning-networks"
title: "Motion Planning Networks"
authors: ["Qureshi, Ahmed H.","Simeonov, Anthony","Bency, Mayur J.","Yip, Michael C."]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1806.05767"
pdf_url: "https://arxiv.org/pdf/1806.05767"
local_pdf: "./2018-motion-planning-networks.pdf"
sha256: "f473ab377fe93612b351a1181c788fd9b8a21d576b5ee699b37bf6bb8c9f0686"
bytes: 1204399
pages: 7
topics: ["planning-control-ik","motion-planning-networks"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode the environment","detail":"Compress an obstacle point cloud into a planning representation.","column":0,"row":0,"section":"Encode the environment","problem_slugs":[],"planned_problems":["Encode Obstacles into a Fixed Feature"]},{"id":"stage-2","title":"Predict bidirectional waypoints","detail":"Grow paths from start and goal toward one another.","column":1,"row":0,"section":"Predict bidirectional waypoints","problem_slugs":[],"planned_problems":["Predict and Validate an Intermediate Waypoint"]},{"id":"stage-3","title":"Validate and repair","detail":"Check every edge and replan infeasible segments.","column":2,"row":0,"section":"Validate and repair","problem_slugs":[],"planned_problems":["Repair an Infeasible Planned Segment"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"environment code"},{"from":"stage-2","to":"stage-3","label":"candidate path"}]}
---

## Core paper explanation

MPNet encodes obstacles and predicts successive path waypoints. Its neural planner proposes paths quickly, while explicit collision checking, path contraction, and replanning handle feasibility.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode the environment

An encoder maps obstacle points $X_{\mathrm{obs}}$ to latent vector $z=E(X_{\mathrm{obs}})$. The representation is trained before the waypoint predictor. Point-cloud coordinates and robot configuration coordinates need a consistent workspace convention.


**Component practice**

- Encode Obstacles into a Fixed Feature — unreviewed idea; contract and evaluator required.

### Predict bidirectional waypoints

A planning network predicts
$$q_{\mathrm{next}}=P_\theta(q_{\mathrm{current}},q_{\mathrm{target}},z).$$
Supervised training uses expert-path next states, with an error such as $\|q_{\mathrm{next}}-q^*\|_2^2$. The bidirectional heuristic alternates growth direction and tries to connect the two partial paths.


**Component practice**

- Predict and Validate an Intermediate Waypoint — unreviewed idea; contract and evaluator required.

### Validate and repair

A path $\tau=(q_0,\ldots,q_H)$ is accepted only if every interpolated edge passes the collision checker. Lazy state contraction shortens unnecessary detours, and replanning repairs invalid segments. Neural output alone is not a certificate of feasibility.


**Component practice**

- Repair an Infeasible Planned Segment — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Encode Obstacles into a Fixed Feature — unreviewed idea; contract and evaluator required.
- Predict and Validate an Intermediate Waypoint — unreviewed idea; contract and evaluator required.
- Repair an Infeasible Planned Segment — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Learned proposals can accelerate repeated planning in familiar environments. Out-of-distribution geometry and narrow passages can defeat the network; preserve the checker and explicit failure return rather than executing an unchecked path.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1806.05767) · [Open-access manuscript](https://arxiv.org/pdf/1806.05767)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
