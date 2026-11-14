---
schema_version: 1
paper_id: "2019-habitat"
title: "Habitat: A Platform for Embodied AI Research"
authors: ["Savva, Manolis","Kadian, Abhishek","Maksymets, Oleksandr","Zhao, Yili","Wijmans, Erik","Jain, Bhavana","Straub, Julian","Liu, Jia","Koltun, Vladlen","Malik, Jitendra","Parikh, Devi","Batra, Dhruv"]
year: 2019
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1904.01201"
pdf_url: "https://arxiv.org/pdf/1904.01201"
local_pdf: "./2019-habitat.pdf"
sha256: "53485f2ed9af000b4f929be140c94e9bc097a59b69a0e5ae847446c0bb947e18"
bytes: 6108339
pages: 17
topics: ["simulation-sim2real","habitat"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Configure agent sensors","detail":"Render observations from a calibrated agent pose.","column":0,"row":0,"section":"Configure agent sensors","problem_slugs":["se3-transform-points"],"planned_problems":["Validate a Navigation Episode"]},{"id":"stage-2","title":"Run a navigation episode","detail":"Follow a task goal using only permitted observations.","column":1,"row":0,"section":"Run a navigation episode","problem_slugs":[],"planned_problems":["Replay a Seeded Navigation Trajectory"]},{"id":"stage-3","title":"Measure success and efficiency","detail":"Use path-length-aware evaluation and held-out scenes.","column":2,"row":0,"section":"Measure success and efficiency","problem_slugs":[],"planned_problems":["Compute Success and SPL"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"sensor observations"},{"from":"stage-2","to":"stage-3","label":"episode paths"}]}
---

## Core paper explanation

Habitat separates fast configurable 3D simulation from task definitions and embodied-agent evaluation. The original paper emphasizes scalable visual navigation and cross-dataset generalization.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Configure agent sensors

A sensor pose composes as $T_{WS}=T_{WA}T_{AS}$, with world $W$, agent $A$, and sensor $S$. Intrinsics, sensor height, action step size, and collision geometry affect navigation difficulty and must be pinned.


**Component practice**

- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate a Navigation Episode — unreviewed idea; contract and evaluator required.

### Run a navigation episode

For start and goal, let $\ell_i$ be shortest feasible path length and $p_i$ the agent's traveled length. Both use the same scene geometry and distance convention. A stop action and success-radius rule determine completion; proximity alone may not satisfy the protocol.


**Component practice**

- Replay a Seeded Navigation Trajectory — unreviewed idea; contract and evaluator required.

### Measure success and efficiency

Success weighted by path length is
$$\mathrm{SPL}=\frac1N\sum_i S_i\frac{\ell_i}{\max(p_i,\ell_i)}.$$
Handle zero-length episodes according to the benchmark specification. SPL combines completion and efficiency but does not measure every safety or exploration property.


**Component practice**

- Compute Success and SPL — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).

**Planned component problems:**

- Validate a Navigation Episode — unreviewed idea; contract and evaluator required.
- Replay a Seeded Navigation Trajectory — unreviewed idea; contract and evaluator required.
- Compute Success and SPL — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Fast navigation simulation enables large experience budgets. Sensor idealization, scene reconstruction gaps, and a mismatch between simulated and real collision geometry can limit transfer.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1904.01201) · [Open-access manuscript](https://arxiv.org/pdf/1904.01201)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
