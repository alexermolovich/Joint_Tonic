---
schema_version: 1
paper_id: "2021-calvin"
title: "CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks"
authors: ["Mees, Oier","Hermann, Lukas","Rosete-Beas, Erick","Burgard, Wolfram"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2112.03227"
pdf_url: "https://arxiv.org/pdf/2112.03227"
local_pdf: "./2021-calvin.pdf"
sha256: "c8ad4741782fa8fb773377fbf61b8772b86574f255599a229d3f6ad4d878c60e"
bytes: 2092247
pages: 10
topics: ["mlops-data-deployment","calvin"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Prepare play and language","detail":"Associate temporally grounded instructions with robot experience.","column":0,"row":0,"section":"Prepare play and language","problem_slugs":["validate-robot-episodes"],"planned_problems":["Validate Language-to-Episode Annotations"]},{"id":"stage-2","title":"Execute instruction chains","detail":"Continue from each achieved task state into the next instruction.","column":1,"row":0,"section":"Execute instruction chains","problem_slugs":[],"planned_problems":["Segment a Long-Horizon Robot Rollout"]},{"id":"stage-3","title":"Measure long-horizon generalization","detail":"Report chain performance on declared environment splits.","column":2,"row":0,"section":"Measure long-horizon generalization","problem_slugs":[],"planned_problems":["Score Chained Task Success"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"language-conditioned policy"},{"from":"stage-2","to":"stage-3","label":"rollout outcomes"}]}
---

## Core paper explanation

CALVIN evaluates language-conditioned manipulation over long sequences in multiple simulated environments. Play data supports learning reusable behaviors, while sequential instruction evaluation exposes error accumulation that isolated tasks can hide.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Prepare play and language

A training segment contains observations $o_{t:t+H}$, actions $a_{t:t+H-1}$, and language $\ell$. Segment boundaries and task annotations must describe the behavior actually visible in that interval. Random frame splits can leak the same play sequence into training and evaluation.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate Language-to-Episode Annotations — unreviewed idea; contract and evaluator required.

### Execute instruction chains

For ordered successes $S_1,\ldots,S_K$, define completed prefix length
$$L=\sum_{k=1}^K\prod_{j=1}^k\mathbf1[S_j].$$
This teaching expression captures consecutive completion: success after an earlier failed task does not extend the prefix. Reset and initial-state rules must match the benchmark protocol.


**Component practice**

- Segment a Long-Horizon Robot Rollout — unreviewed idea; contract and evaluator required.

### Measure long-horizon generalization

Average chain length is $\bar L=N^{-1}\sum_iL_i$. Also report $P(L\ge k)$ for each depth. These values expose compounding failures; they are not equivalent to independently averaging single-task success rates.


**Component practice**

- Score Chained Task Success — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).

**Planned component problems:**

- Validate Language-to-Episode Annotations — unreviewed idea; contract and evaluator required.
- Segment a Long-Horizon Robot Rollout — unreviewed idea; contract and evaluator required.
- Score Chained Task Success — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Long-horizon manipulation needs each completed action to leave a state suitable for the next. Small positioning errors, language ambiguity, and recovery failures accumulate even when individual skills look reliable.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2112.03227) · [Open-access manuscript](https://arxiv.org/pdf/2112.03227)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
