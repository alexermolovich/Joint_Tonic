---
schema_version: 1
paper_id: "2019-rlbench"
title: "RLBench: The Robot Learning Benchmark & Learning Environment"
authors: ["James, Stephen","Ma, Zicong","Arrojo, David Rovick","Davison, Andrew J."]
year: 2019
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1909.12271"
pdf_url: "https://arxiv.org/pdf/1909.12271"
local_pdf: "./2019-rlbench.pdf"
sha256: "fbb04509bea7bf6aa9b97b07c46d95e5c1a900987599693b3fae3fd84377db76"
bytes: 3732227
pages: 8
topics: ["simulation-sim2real","rlbench"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Instantiate a task variation","detail":"Set objects, language descriptions, and valid initial conditions.","column":0,"row":0,"section":"Instantiate a task variation","problem_slugs":[],"planned_problems":["Build a Task-Variation Sampler"]},{"id":"stage-2","title":"Generate demonstrations","detail":"Use authored waypoints and motion planning to collect trajectories.","column":1,"row":0,"section":"Generate demonstrations","problem_slugs":["validate-robot-episodes"],"planned_problems":["Validate Demonstration Waypoints"]},{"id":"stage-3","title":"Evaluate held-out behavior","detail":"Measure task success under the declared observation and action interface.","column":2,"row":0,"section":"Evaluate held-out behavior","problem_slugs":[],"planned_problems":["Score Multi-Stage Task Completion"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"task instance"},{"from":"stage-2","to":"stage-3","label":"policy rollouts"}]}
---

## Core paper explanation

RLBench provides manipulation tasks, variations, visual/proprioceptive observations, and planner-generated demonstrations. Task waypoints and success conditions make demonstrations reproducible while keeping learning methods independent of the data generator.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Instantiate a task variation

A reproducible instance is $(\mathrm{task},\mathrm{variation},\mathrm{seed},\mathrm{assets})$. This tuple is a teaching provenance contract. Variations may change object identity, color, placement, or other task parameters; they are not necessarily independent tasks.


**Component practice**

- Build a Task-Variation Sampler — unreviewed idea; contract and evaluator required.

### Generate demonstrations

A planned path $q_{0:H}$ must satisfy collision and task constraints throughout execution. Store observations and actions at the controller timestep, not only sparse waypoints. A waypoint path is privileged generation information and should not become a learner input unless the experiment explicitly permits it.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate Demonstration Waypoints — unreviewed idea; contract and evaluator required.

### Evaluate held-out behavior

Success rate is $\hat p=N^{-1}\sum_iS_i$, with $S_i$ computed by task-specific predicates. Report task/variation splits and action mode. Comparing joint-velocity and end-effector-pose policies without naming their controllers hides materially different problems.


**Component practice**

- Score Multi-Stage Task Completion — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).

**Planned component problems:**

- Build a Task-Variation Sampler — unreviewed idea; contract and evaluator required.
- Validate Demonstration Waypoints — unreviewed idea; contract and evaluator required.
- Score Multi-Stage Task Completion — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Standardized demonstrations support reproducible imitation learning. Planner trajectories can omit human-like recovery and contain privileged geometric assumptions that a visual policy must still learn to handle.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1909.12271) · [Open-access manuscript](https://arxiv.org/pdf/1909.12271)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
