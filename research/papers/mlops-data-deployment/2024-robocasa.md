---
schema_version: 1
paper_id: "2024-robocasa"
title: "RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots"
authors: ["Nasiriany, Soroush","Maddukuri, Abhiram","Zhang, Lance","Parikh, Adeet","Lo, Aaron","Joshi, Abhishek","Mandlekar, Ajay","Zhu, Yuke"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2406.02523"
pdf_url: "https://arxiv.org/pdf/2406.02523"
local_pdf: "./2024-robocasa.pdf"
sha256: "7aca93ca3f157e32a46e02d675b3b2c24e3073a7807c038f7f566b73db87bde3"
bytes: 8307032
pages: 16
topics: ["mlops-data-deployment","robocasa"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title": "Core execution flow", "description": "Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.", "nodes": [{"id": "stage-1", "title": "Generate a scenario", "detail": "Choose scene layout, objects, task, and embodiment.", "column": 0, "row": 0, "section": "Generate a scenario", "problem_slugs": [], "planned_problems": ["Validate a Kitchen Scenario Configuration", "Stratify Tasks by Scene Factors"]}, {"id": "stage-2", "title": "Produce demonstrations", "detail": "Collect or synthesize trajectories under explicit success conditions.", "column": 1, "row": 0, "section": "Produce demonstrations", "problem_slugs": [], "planned_problems": ["Validate a Teleoperation Demonstration"]}, {"id": "stage-3", "title": "Evaluate variation and transfer", "detail": "Hold out meaningful scene factors and test real-world relevance separately.", "column": 2, "row": 0, "section": "Evaluate variation and transfer", "problem_slugs": ["scenario-coverage-confidence", "version-simulation-distribution"], "planned_problems": ["Aggregate Generalization Across Scene Families"]}], "edges": [{"from": "stage-1", "to": "stage-2", "label": "configured scene"}, {"from": "stage-2", "to": "stage-3", "label": "scenario trajectories"}]}
---

## Core paper explanation

RoboCasa provides diverse simulated everyday manipulation environments, assets, tasks, and generated demonstrations. Its purpose is to scale structured robot learning experience beyond a small collection of repeated tabletop scenes.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Generate a scenario

Write a scenario as $z=(\mathrm{layout},\mathrm{objects},\mathrm{task},\mathrm{robot},\mathrm{seed})$. This is a teaching reproducibility record, not a paper-specific model equation. Asset versions, placements, and physics settings are needed to reconstruct the same episode.


**Component practice**

- Validate a Kitchen Scenario Configuration — unreviewed idea; contract and evaluator required.
- Stratify Tasks by Scene Factors — unreviewed idea; contract and evaluator required.

### Produce demonstrations

A task predicate $S(s_{0:T})\in\{0,1\}$ should encode the intended completion condition. Checking only a final object location can miss prohibited intermediate contacts or invalid grasp behavior. Preserve failed generation attempts to distinguish filtering from policy capability.


**Component practice**

- Validate a Teleoperation Demonstration — unreviewed idea; contract and evaluator required.

### Evaluate variation and transfer

For scenario distribution $p(z)$, expected simulated success is $\mathbb E_{z\sim p}\mathbb E[S\mid z]$. This formalizes what a benchmark average measures. Changing the scenario distribution changes the meaning of the score; real-world transfer requires additional physical experiments.



<!-- joint-tonic-math-expansion -->
#### Specify the scenario distribution behind the score

Suppose scene family $j$ has $n_j>0$ evaluation episodes and successes $S_{ji}\in\{0,1\}$. Let $w_j\ge0$ be declared family weights summing to one. An original reporting model is

$$\widehat p_j=\frac1{n_j}\sum_{i=1}^{n_j}S_{ji},\qquad \widehat p_{\mathrm{target}}=\sum_{j=1}^{J}w_j\widehat p_j.$$

Uniform family weights answer a different question from pooling every episode. If family A has 9/10 successes and B has 1/2, pooled success is 10/12, while equal-family success is $(0.9+0.5)/2=0.7$. Neither is universally correct; the intended deployment distribution determines the relevant weights. Missing families must be reported rather than assigned an invented success rate.

[Scenario coverage with confidence intervals](/problems/scenario-coverage-confidence) makes unobserved buckets explicit. [Version a scenario distribution](/problems/version-simulation-distribution) demonstrates a reproducible bounded distribution declaration; it does not encode every RoboCasa asset/task parameter or run the simulator.
<!-- /joint-tonic-math-expansion -->

**Component practice**

- Aggregate Generalization Across Scene Families — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Validate a Kitchen Scenario Configuration — unreviewed idea; contract and evaluator required.
- Stratify Tasks by Scene Factors — unreviewed idea; contract and evaluator required.
- Validate a Teleoperation Demonstration — unreviewed idea; contract and evaluator required.
- Aggregate Generalization Across Scene Families — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Diverse kitchens and objects can expand training coverage. Visual realism does not guarantee accurate friction, articulation, or contact dynamics; simulation diversity and physical fidelity solve different problems.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2406.02523) · [Open-access manuscript](https://arxiv.org/pdf/2406.02523)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
