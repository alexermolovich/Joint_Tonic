---
schema_version: 1
paper_id: "2021-habitat-2"
title: "Habitat 2.0: Training Home Assistants to Rearrange their Habitat"
authors: ["Szot, Andrew","Clegg, Alex","Undersander, Eric","Wijmans, Erik","Zhao, Yili","Turner, John","Maestre, Noah","Mukadam, Mustafa","Chaplot, Devendra","Maksymets, Oleksandr","Gokaslan, Aaron","Vondrus, Vladimir","Dharur, Sameer","Meier, Franziska","Galuba, Wojciech","Chang, Angel","Kira, Zsolt","Koltun, Vladlen","Malik, Jitendra","Savva, Manolis","Batra, Dhruv"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2106.14405"
pdf_url: "https://arxiv.org/pdf/2106.14405"
local_pdf: "./2021-habitat-2.pdf"
sha256: "92f9c30479fe4203f656c218fa228c7e5fd71f23a9821b3afa47e06dbe5ab317"
bytes: 45408472
pages: 32
topics: ["simulation-sim2real","habitat-2"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Configure a rearrangement task","detail":"Set object, receptacle, articulation, and robot states.","column":0,"row":0,"section":"Configure a rearrangement task","problem_slugs":[],"planned_problems":["Construct a Rearrangement Goal Graph","Validate Object Reset States"]},{"id":"stage-2","title":"Compose skills","detail":"Transfer control between navigation, grasping, and placement.","column":1,"row":0,"section":"Compose skills","problem_slugs":[],"planned_problems":["Validate Skill Preconditions in a Rearrangement Plan"]},{"id":"stage-3","title":"Evaluate long-horizon outcomes","detail":"Measure task completion and diagnose handoff failures.","column":2,"row":0,"section":"Evaluate long-horizon outcomes","problem_slugs":[],"planned_problems":["Score Chained Task Success"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"task state"},{"from":"stage-2","to":"stage-3","label":"skill sequence"}]}
---

## Core paper explanation

Habitat 2.0 adds physics-enabled rearrangement, reconfigurable articulated indoor scenes, and long-horizon mobile-manipulation benchmarks. It evaluates both learned policies and classical sense-plan-act pipelines.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Configure a rearrangement task

A target can require $\|p_o-p_o^*\|_2<\epsilon$ together with predicates for placement, release, or articulation. This is a teaching goal model; official tasks have their own conditions. Navigation and manipulation share one evolving scene state.


**Component practice**

- Construct a Rearrangement Goal Graph — unreviewed idea; contract and evaluator required.
- Validate Object Reset States — unreviewed idea; contract and evaluator required.


### Compose skills

For skill $k$, a termination set $\mathcal T_k$ must produce states inside the next skill's valid initiation set $\mathcal I_{k+1}$. The inclusion $\mathcal T_k\subseteq\mathcal I_{k+1}$ is an ideal compositional contract, not an automatic property of independently trained skills.


**Component practice**

- Validate Skill Preconditions in a Rearrangement Plan — unreviewed idea; contract and evaluator required.


### Evaluate long-horizon outcomes

Whole-task success is $S=\prod_kS_k$ only when each $S_k$ captures the required sequential condition. Report where failures occur and whether objects, receptacles, or layouts are held out. High skill success in isolation can coexist with poor composed performance.


**Component practice**

- Score Chained Task Success — unreviewed idea; contract and evaluator required.


## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Construct a Rearrangement Goal Graph — unreviewed idea; contract and evaluator required.
- Validate Object Reset States — unreviewed idea; contract and evaluator required.
- Validate Skill Preconditions in a Rearrangement Plan — unreviewed idea; contract and evaluator required.
- Score Chained Task Success — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

The benchmark exposes practical dependencies between locomotion and manipulation. A grasp reached from the wrong base pose or an incomplete release can invalidate later skills even when each local controller appears competent.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2106.14405) · [Open-access manuscript](https://arxiv.org/pdf/2106.14405)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
