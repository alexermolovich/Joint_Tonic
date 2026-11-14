---
schema_version: 1
paper_id: "2018-datasheets-for-datasets"
title: "Datasheets for Datasets"
authors: ["Gebru, Timnit","Morgenstern, Jamie","Vecchione, Briana","Vaughan, Jennifer Wortman","Wallach, Hanna","Daumé III, Hal","Crawford, Kate"]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1803.09010"
pdf_url: "https://arxiv.org/pdf/1803.09010"
local_pdf: "./2018-datasheets-for-datasets.pdf"
sha256: "c7f595988ee2c109631d5173fdae37ff1774c68ec17add51bd012f2a6e8792d0"
bytes: 554802
pages: 18
topics: ["mlops-data-deployment","datasheets-for-datasets"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Record collection context","detail":"Describe motivation, population, acquisition, and permissions.","column":0,"row":0,"section":"Record collection context","problem_slugs":[],"planned_problems":["Validate a Robot Dataset Datasheet","Detect Missing Provenance Fields"]},{"id":"stage-2","title":"Describe composition and gaps","detail":"Quantify coverage while preserving qualitative limitations.","column":1,"row":0,"section":"Describe composition and gaps","problem_slugs":[],"planned_problems":["Compute Collector and Task Coverage"]},{"id":"stage-3","title":"Publish maintenance guidance","detail":"Document intended uses, distribution, updates, and known risks.","column":2,"row":0,"section":"Publish maintenance guidance","problem_slugs":[],"planned_problems":["Generate a Data-Use Risk Report"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"documented records"},{"from":"stage-2","to":"stage-3","label":"dataset description"}]}
---

## Core paper explanation

Datasheets for Datasets proposes structured documentation of why a dataset exists, what it contains, how it was collected and processed, and which uses are appropriate. It is a documentation framework, not a new numeric learning algorithm.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Record collection context

For robotics, record embodiment, sensors, calibration, operators, environments, and collection policy. A teaching lineage relation is $D_{v+1}=F_v(D_v)$, where $F_v$ names the exact filtering/labeling transform. This formalizes traceability; it is not an equation proposed by the paper.


**Component practice**

- Validate a Robot Dataset Datasheet — unreviewed idea; contract and evaluator required.
- Detect Missing Provenance Fields — unreviewed idea; contract and evaluator required.

### Describe composition and gaps

For declared slice $s$, report $n_s=\sum_i\mathbf1[x_i\in s]$ and fraction $n_s/N$. Overlapping slices need not sum to $N$. Counts do not prove representative sampling, consent, or suitability. State missing metadata explicitly rather than treating unknown values as negative answers.


**Component practice**

- Compute Collector and Task Coverage — unreviewed idea; contract and evaluator required.

### Publish maintenance guidance

A dataset version should identify its datasheet, split definitions, processing history, and change policy. Documentation questions may be inapplicable, but omission should be deliberate. The framework supports reflection and accountability; a completed checklist is not a certification of dataset quality.


**Component practice**

- Generate a Data-Use Risk Report — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Validate a Robot Dataset Datasheet — unreviewed idea; contract and evaluator required.
- Detect Missing Provenance Fields — unreviewed idea; contract and evaluator required.
- Compute Collector and Task Coverage — unreviewed idea; contract and evaluator required.
- Generate a Data-Use Risk Report — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Robot data is inseparable from collection conditions. A dataset with many episodes may omit rare contacts, calibration drift, or recovery behavior; those gaps should be visible before model training.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1803.09010) · [Open-access manuscript](https://arxiv.org/pdf/1803.09010)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
