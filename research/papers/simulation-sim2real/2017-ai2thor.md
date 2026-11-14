---
schema_version: 1
paper_id: "2017-ai2thor"
title: "AI2-THOR: An Interactive 3D Environment for Visual AI"
authors: ["Kolve, Eric","Mottaghi, Roozbeh","Han, Winson","VanderBilt, Eli","Weihs, Luca","Herrasti, Alvaro","Deitke, Matt","Ehsani, Kiana","Gordon, Daniel","Zhu, Yuke","Kembhavi, Aniruddha","Gupta, Abhinav","Farhadi, Ali"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1712.05474"
pdf_url: "https://arxiv.org/pdf/1712.05474"
local_pdf: "./2017-ai2thor.pdf"
sha256: "8495e92c940ce2366ba4b015eff90c0b3763c92af86abb06ba1acc38c36ae242"
bytes: 9242723
pages: 12
topics: ["simulation-sim2real","ai2thor"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Observe scene and objects","detail":"Expose camera observations and declared object state.","column":0,"row":0,"section":"Observe scene and objects","problem_slugs":[],"planned_problems":["Track Object-State Preconditions"]},{"id":"stage-2","title":"Apply a valid interaction","detail":"Check action preconditions and report success or failure.","column":1,"row":0,"section":"Apply a valid interaction","problem_slugs":[],"planned_problems":["Validate a Simulator Action Grammar"]},{"id":"stage-3","title":"Evaluate embodied tasks","detail":"Measure goal completion with controlled scene splits.","column":2,"row":0,"section":"Evaluate embodied tasks","problem_slugs":[],"planned_problems":["Detect an Invalid Interaction Transition"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"selected action"},{"from":"stage-2","to":"stage-3","label":"interaction trace"}]}
---

## Core paper explanation

AI2-THOR provides interactive indoor scenes where an agent can navigate and change object states. Its useful learning boundary is the relationship between visual observations, action preconditions, and environment transitions.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Observe scene and objects

A partially observed interaction model is $o_t\sim O(\cdot\mid s_t)$, where $s_t$ includes object poses and state such as open/closed. This is a teaching formalization of the simulator interface, not a new algorithm from the paper. Hidden simulator metadata must not silently become policy input.


**Component practice**

- Track Object-State Preconditions — unreviewed idea; contract and evaluator required.

### Apply a valid interaction

An action $a$ has a precondition $P_a(s)$ and transition $s'=F(s,a)$ when valid. Opening an object and picking it up are different state changes. An invalid action should produce an explicit outcome; assuming every command changes the world corrupts training labels.


**Component practice**

- Validate a Simulator Action Grammar — unreviewed idea; contract and evaluator required.

### Evaluate embodied tasks

For goal predicate $G$, episode success is $S=\mathbf1[G(s_T)]$. Additional efficiency metrics require a stated action budget and reset protocol. Hold out scenes or object configurations to test generalization rather than repeated memorization.


**Component practice**

- Detect an Invalid Interaction Transition — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Track Object-State Preconditions — unreviewed idea; contract and evaluator required.
- Validate a Simulator Action Grammar — unreviewed idea; contract and evaluator required.
- Detect an Invalid Interaction Transition — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Interactive simulation exposes causal object-state changes absent from static images. Discrete actions and idealized preconditions can hide real controller and contact failures, so transfer claims need physical evaluation.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1712.05474) · [Open-access manuscript](https://arxiv.org/pdf/1712.05474)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
