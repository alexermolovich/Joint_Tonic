---
schema_version: 1
paper_id: "2018-roboturk"
title: "RoboTurk: A Crowdsourcing Platform for Robotic Skill Learning through Imitation"
authors: ["Mandlekar, Ajay","Zhu, Yuke","Garg, Animesh","Booher, Jonathan","Spero, Max","Tung, Albert","Gao, Julian","Emmons, John","Gupta, Anchit","Orbay, Emre","Savarese, Silvio","Fei-Fei, Li"]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1811.02790"
pdf_url: "https://arxiv.org/pdf/1811.02790"
local_pdf: "./2018-roboturk.pdf"
sha256: "2298863a8e3aa917506ae8583cadc6741a557eb9809f976101a4fd3119c3303d"
bytes: 3606292
pages: 15
topics: ["mlops-data-deployment","roboturk"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Map operator motion","detail":"Translate mobile-device motion into a robot control reference.","column":0,"row":0,"section":"Map operator motion","problem_slugs":["se3-transform-points"],"planned_problems":["Map Operator Motion into a Robot Control Frame"]},{"id":"stage-2","title":"Stream control and feedback","detail":"Run a session with synchronized actions and visual observations.","column":1,"row":0,"section":"Stream control and feedback","problem_slugs":[],"planned_problems":["Detect Paused or Corrupted Action Segments"]},{"id":"stage-3","title":"Curate demonstrations","detail":"Store complete episodes and task outcomes for learning.","column":2,"row":0,"section":"Curate demonstrations","problem_slugs":["validate-robot-episodes"],"planned_problems":["Validate a Teleoperation Demonstration","Compute Collector and Task Coverage"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"operator commands"},{"from":"stage-2","to":"stage-3","label":"session trajectories"}]}
---

## Core paper explanation

RoboTurk supports scalable robot demonstration collection through commodity mobile-device teleoperation and remote visual feedback. Its contribution is a collection platform and interface, with demonstration quality and usability evaluated experimentally.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Map operator motion

A teaching relative-pose interface uses $\Delta T=T_{\mathrm{phone},0}^{-1}T_{\mathrm{phone},t}$, then maps that displacement into the robot's controller frame. The exact scaling, clutching, and orientation conventions belong to the teleoperation interface; raw phone coordinates are not robot coordinates.


**Component practice**

- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Map Operator Motion into a Robot Control Frame — unreviewed idea; contract and evaluator required.

### Stream control and feedback

End-to-end feedback age is $\Delta t=t_{\mathrm{display}}-t_{\mathrm{capture}}$. This diagnostic includes capture, transport, processing, and display delay. The paper studies operation under network variation; it does not establish arbitrary latency tolerance for every robot task.


**Component practice**

- Detect Paused or Corrupted Action Segments — unreviewed idea; contract and evaluator required.

### Curate demonstrations

An episode is a time-ordered sequence $(o_t,a_t,t_t)$ with task metadata and termination outcome. Validate monotonic timestamps, action units, missing frames, and successful/failed completion labels. Collection infrastructure and downstream imitation-learning results are separate evaluation layers.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate a Teleoperation Demonstration — unreviewed idea; contract and evaluator required.
- Compute Collector and Task Coverage — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).
- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).

**Planned component problems:**

- Map Operator Motion into a Robot Control Frame — unreviewed idea; contract and evaluator required.
- Detect Paused or Corrupted Action Segments — unreviewed idea; contract and evaluator required.
- Validate a Teleoperation Demonstration — unreviewed idea; contract and evaluator required.
- Compute Collector and Task Coverage — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Accessible teleoperation can broaden demonstration coverage. Network jitter, operator differences, and controller saturation change the recorded action distribution; retain these collection conditions instead of flattening all trajectories into identical examples.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1811.02790) · [Open-access manuscript](https://arxiv.org/pdf/1811.02790)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
