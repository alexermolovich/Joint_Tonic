---
schema_version: 1
paper_id: "2020-igibson"
title: "iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes"
authors: ["Shen, Bokui","Xia, Fei","Li, Chengshu","Martín-Martín, Roberto","Fan, Linxi","Wang, Guanzhi","Pérez-D'Arpino, Claudia","Buch, Shyamal","Srivastava, Sanjana","Tchapmi, Lyne P.","Tchapmi, Micael E.","Vainio, Kent","Wong, Josiah","Fei-Fei, Li","Savarese, Silvio"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2012.02924"
pdf_url: "https://arxiv.org/pdf/2012.02924"
local_pdf: "./2020-igibson.pdf"
sha256: "6b6840463b960afe2f2a095470a90029ff41f0cc26f4717509cb67a1d424d61c"
bytes: 4704504
pages: 11
topics: ["simulation-sim2real","igibson"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title": "Core execution flow", "description": "Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.", "nodes": [{"id": "stage-1", "title": "Build an interactive scene", "detail": "Load rigid and articulated assets with physical properties.", "column": 0, "row": 0, "section": "Build an interactive scene", "problem_slugs": [], "planned_problems": ["Validate a Scene Interaction Graph"]}, {"id": "stage-2", "title": "Randomize and observe", "detail": "Vary visual and physical conditions while generating sensor data.", "column": 1, "row": 0, "section": "Randomize and observe", "problem_slugs": ["validate-robot-episodes", "seeded-visual-randomization", "sample-dynamics-distributions"], "planned_problems": ["Replay Sensor Streams from a Fixed Seed"]}, {"id": "stage-3", "title": "Interact and evaluate transfer", "detail": "Test tasks on declared scene and parameter holdouts.", "column": 2, "row": 0, "section": "Interact and evaluate transfer", "problem_slugs": [], "planned_problems": ["Measure Domain Shift Between Simulated Scenes"]}], "edges": [{"from": "stage-1", "to": "stage-2", "label": "scene state"}, {"from": "stage-2", "to": "stage-3", "label": "policy actions"}]}
---

## Core paper explanation

iGibson 1.0 combines interactive indoor scenes, articulated objects, virtual sensors, domain randomization, and planning interfaces. It supports studying navigation and manipulation in environments whose objects can physically change state.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Build an interactive scene

An articulated object state contains joint coordinates $q_o$ in addition to its base pose. A door hinge angle and a drawer displacement have different units. Collision geometry, mass, friction, and joint limits are part of the scene contract.


**Component practice**

- Validate a Scene Interaction Graph — unreviewed idea; contract and evaluator required.

### Randomize and observe

Training samples parameters $\theta\sim p(\theta)$ and observations from the resulting environment. A teaching objective is $\mathbb E_{\theta,\tau\sim\pi,P_\theta}[R(\tau)]$. Appearance randomization and dynamics randomization alter different parts of the agent's problem.



<!-- joint-tonic-math-expansion -->
#### Separate appearance from transition changes

Let $\theta_v$ denote visual parameters (lighting/textures/camera) and $\theta_d$ physical parameters (mass/friction/actuation). A teaching factorization is

$$s_{t+1}\sim P_{\theta_d}(\cdot\mid s_t,a_t),\qquad o_t\sim O_{\theta_v}(\cdot\mid s_t).$$

State $s_t$ contains poses and articulated joint coordinates; observation $o_t$ may include RGB/depth/proprioception with separately declared units. This separation is conceptual: camera placement can affect observability, and a complete simulator may couple some parameters. Increasing texture brightness need not change a rigid body's trajectory; changing friction may change both its trajectory and resulting images.

For independently sampled scenarios $\theta_i$ and episodic returns $R_i$, a Monte Carlo mean is $\bar R=N^{-1}\sum_iR_i$. The randomization distribution defines what this average measures. [Seeded visual sampling](/problems/seeded-visual-randomization) and [dynamics sampling](/problems/sample-dynamics-distributions) implement separate bounded parameter contracts, not iGibson's complete configuration system.
<!-- /joint-tonic-math-expansion -->

**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Replay Sensor Streams from a Fixed Seed — unreviewed idea; contract and evaluator required.

### Interact and evaluate transfer

Evaluate success by scene and interaction type, not only pooled episode count. Keep randomization seeds and distributions attached to trajectories. Motion-planning demonstrations and learned policies can share task interfaces while using different information during generation.


**Component practice**

- Measure Domain Shift Between Simulated Scenes — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).

**Planned component problems:**

- Validate a Scene Interaction Graph — unreviewed idea; contract and evaluator required.
- Replay Sensor Streams from a Fixed Seed — unreviewed idea; contract and evaluator required.
- Measure Domain Shift Between Simulated Scenes — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Interactive homes expose dependencies such as opening a door before passing through it. Asset realism does not ensure correct hinge friction, contact forces, or real sensor noise.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2012.02924) · [Open-access manuscript](https://arxiv.org/pdf/2012.02924)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
