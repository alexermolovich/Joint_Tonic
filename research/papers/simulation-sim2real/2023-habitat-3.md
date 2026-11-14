---
schema_version: 1
paper_id: "2023-habitat-3"
title: "Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots"
authors: ["Puig, Xavier","Undersander, Eric","Szot, Andrew","Cote, Mikael Dallaire","Yang, Tsung-Yen","Partsey, Ruslan","Desai, Ruta","Clegg, Alexander William","Hlavac, Michal","Min, So Yeon","Vondruš, Vladimír","Gervet, Theophile","Berges, Vincent-Pierre","Turner, John M.","Maksymets, Oleksandr","Kira, Zsolt","Kalakrishnan, Mrinal","Malik, Jitendra","Chaplot, Devendra Singh","Jain, Unnat","Batra, Dhruv","Rai, Akshara","Mottaghi, Roozbeh"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2310.13724"
pdf_url: "https://arxiv.org/pdf/2310.13724"
local_pdf: "./2023-habitat-3.pdf"
sha256: "6383018901acbf7677050585da9a30707437cf7119def797be500f33a68021af"
bytes: 8852187
pages: 30
topics: ["simulation-sim2real","habitat-3"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title": "Core execution flow", "description": "Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.", "nodes": [{"id": "stage-1", "title": "Represent both agents", "detail": "Track robot, human, and shared scene state.", "column": 0, "row": 0, "section": "Represent both agents", "problem_slugs": [], "planned_problems": ["Synchronize Human and Robot Agent States"]}, {"id": "stage-2", "title": "Coordinate interaction", "detail": "Navigate or rearrange while responding to a partner.", "column": 1, "row": 0, "section": "Coordinate interaction", "problem_slugs": [], "planned_problems": ["Measure Human-Robot Proximity Events"]}, {"id": "stage-3", "title": "Evaluate collaboration", "detail": "Measure task outcomes with unseen partners and human participants.", "column": 2, "row": 0, "section": "Evaluate collaboration", "problem_slugs": ["shift-bucket-performance", "scenario-coverage-confidence"], "planned_problems": ["Evaluate a Cooperative Interaction Episode"]}], "edges": [{"from": "stage-1", "to": "stage-2", "label": "joint scene"}, {"from": "stage-2", "to": "stage-3", "label": "interaction episodes"}]}
---

## Core paper explanation

Habitat 3.0 supports collaborative human–robot tasks with simulated humanoids and human-in-the-loop interfaces. Social navigation and rearrangement evaluate how a robot responds to partners whose behavior changes the environment.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Represent both agents

A joint transition model is $s_{t+1}\sim P(\cdot\mid s_t,a_t^R,a_t^H)$. The robot observes only its permitted sensory context, not necessarily the human's full intent. This is a teaching multi-agent formalization of the platform.


**Component practice**

- Synchronize Human and Robot Agent States — unreviewed idea; contract and evaluator required.

### Coordinate interaction

A diagnostic separation is $d_t=\|p_t^R-p_t^H\|_2$ in meters. Distance alone is insufficient: relative velocity, occlusion, blocking, and task role matter. Simulated partner policies and real human input produce different behavior distributions.


**Component practice**

- Measure Human-Robot Proximity Events — unreviewed idea; contract and evaluator required.

### Evaluate collaboration

Report completion and interaction failures by partner type. A teaching average $\mathbb E_{h\sim p(h)}[S\mid h]$ depends on the tested partner distribution $p(h)$. Efficient completion does not establish comfort or social acceptability; those require their own evaluation.



<!-- joint-tonic-math-expansion -->
#### A partner mixture changes the reported result

Let partner class h have declared deployment weight $w_h\ge0$, with $\sum_hw_h=1$, and measured conditional success $\widehat p_h$. An original evaluation formalization is

$$\widehat p_{\mathrm{mix}}=\sum_hw_h\widehat p_h.$$

For two partner classes with success 0.9 and 0.5, equal weights yield 0.7; weights 0.8/0.2 yield 0.82. Reporting only the pooled score can conceal a failure for the less frequent partner class. Neither score captures comfort, yielding behavior, or collision risk without separate metrics.

An instantaneous separation $d_t=\|p_t^R-p_t^H\|_2$ uses robot/human positions in the same world frame, in metres. A minimum-distance threshold is an operational diagnostic, not a universal social-safety boundary. [Performance by shift bucket](/problems/shift-bucket-performance) and [scenario coverage](/problems/scenario-coverage-confidence) implement bounded per-slice summaries; partner policy design remains outside those exercises.
<!-- /joint-tonic-math-expansion -->

**Component practice**

- Evaluate a Cooperative Interaction Episode — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Synchronize Human and Robot Agent States — unreviewed idea; contract and evaluator required.
- Measure Human-Robot Proximity Events — unreviewed idea; contract and evaluator required.
- Evaluate a Cooperative Interaction Episode — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Human collaboration requires adapting to other agents rather than treating them as static obstacles. A policy that succeeds with predictable simulated partners can fail when a person pauses, changes goals, or takes an unexpected route.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2310.13724) · [Open-access manuscript](https://arxiv.org/pdf/2310.13724)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
