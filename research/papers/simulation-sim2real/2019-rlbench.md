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
execution_flow: {"title": "Core execution flow", "description": "Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.", "nodes": [{"id": "stage-1", "title": "Instantiate a task variation", "detail": "Set objects, language descriptions, and valid initial conditions.", "column": 0, "row": 0, "section": "Instantiate a task variation", "problem_slugs": [], "planned_problems": ["Build a Task-Variation Sampler"]}, {"id": "stage-2", "title": "Generate demonstrations", "detail": "Use authored waypoints and motion planning to collect trajectories.", "column": 1, "row": 0, "section": "Generate demonstrations", "problem_slugs": ["validate-robot-episodes", "time-parameterized-trajectory", "joint-limit-collision-ik-candidates"], "planned_problems": ["Validate Demonstration Waypoints"]}, {"id": "stage-3", "title": "Evaluate held-out behavior", "detail": "Measure task success under the declared observation and action interface.", "column": 2, "row": 0, "section": "Evaluate held-out behavior", "problem_slugs": ["scenario-coverage-confidence"], "planned_problems": ["Score Multi-Stage Task Completion"]}], "edges": [{"from": "stage-1", "to": "stage-2", "label": "task instance"}, {"from": "stage-2", "to": "stage-3", "label": "policy rollouts"}]}
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



<!-- joint-tonic-math-expansion -->
#### Waypoints are not controller-rate trajectories

For joint waypoints $q_k\in\mathbb R^D$ in radians at strictly increasing times $t_k$ seconds, linear interpolation within one interval gives

$$q(t)=(1-\alpha)q_k+\alpha q_{k+1},\qquad\alpha=\frac{t-t_k}{t_{k+1}-t_k}.$$

Its segment velocity is $(q_{k+1}-q_k)/(t_{k+1}-t_k)$ in rad/s. A joint moving from 0 to 1 rad over 2 seconds is at 0.25 rad at 0.5 seconds, with segment speed 0.5 rad/s. This is an original interpolation example, not RLBench's full motion planner or the guarantee that an interpolated path is collision-free.

[Time-parameterized trajectories](/problems/time-parameterized-trajectory) implements this bounded step. [Collision-aware IK candidate selection](/problems/joint-limit-collision-ik-candidates) checks static planar candidates only; a full demonstration generator must check the swept motion and actual 3D collision geometry.
<!-- /joint-tonic-math-expansion -->

**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate Demonstration Waypoints — unreviewed idea; contract and evaluator required.

### Evaluate held-out behavior

Success rate is $\hat p=N^{-1}\sum_iS_i$, with $S_i$ computed by task-specific predicates. Report task/variation splits and action mode. Comparing joint-velocity and end-effector-pose policies without naming their controllers hides materially different problems.



<!-- joint-tonic-math-expansion -->
For task j with $n_j$ independent evaluated episodes, report successes $k_j$ and rate $k_j/n_j$ together. A task with 1/1 success and one with 90/100 should not be interpreted as equally certain. [Scenario confidence intervals](/problems/scenario-coverage-confidence) supplies a marginal binomial interval per declared task/variation bucket; it does not establish performance on unseen variations.
<!-- /joint-tonic-math-expansion -->

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
