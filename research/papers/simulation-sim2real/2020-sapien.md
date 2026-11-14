---
schema_version: 1
paper_id: "2020-sapien"
title: "SAPIEN: A SimulAted Part-based Interactive ENvironment"
authors: ["Xiang, Fanbo","Qin, Yuzhe","Mo, Kaichun","Xia, Yikuan","Zhu, Hao","Liu, Fangchen","Liu, Minghua","Jiang, Hanxiao","Yuan, Yifu","Wang, He","Yi, Li","Chang, Angel X.","Guibas, Leonidas J.","Su, Hao"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2003.08515"
pdf_url: "https://arxiv.org/pdf/2003.08515"
local_pdf: "./2020-sapien.pdf"
sha256: "03aa9317d6e6fe091e724d2b2114143f9da4bc72fa723a7122bcf2cec15057ce"
bytes: 9807939
pages: 16
topics: ["simulation-sim2real","sapien"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title": "Core execution flow", "description": "Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.", "nodes": [{"id": "stage-1", "title": "Represent articulated assets", "detail": "Describe links, joints, and motion constraints.", "column": 0, "row": 0, "section": "Represent articulated assets", "problem_slugs": ["se3-transform-points"], "planned_problems": ["Validate an Articulated Object Schema", "Compute Joint-Conditioned Object State"]}, {"id": "stage-2", "title": "Render part-level observations", "detail": "Generate visual evidence for parts and articulation.", "column": 1, "row": 0, "section": "Render part-level observations", "problem_slugs": ["project-camera-points", "unproject-depth-map", "trace-perception-frame-graph", "geometric-jacobian-joint-axes"], "planned_problems": ["Project a Tracked Point Across Views"]}, {"id": "stage-3", "title": "Test interactive behavior", "detail": "Evaluate whether perception supports the intended object motion.", "column": 2, "row": 0, "section": "Test interactive behavior", "problem_slugs": [], "planned_problems": ["Build a Reproducible Interaction Scenario"]}], "edges": [{"from": "stage-1", "to": "stage-2", "label": "articulated state"}, {"from": "stage-2", "to": "stage-3", "label": "estimated parts and actions"}]}
---

## Core paper explanation

SAPIEN focuses on physically interactive articulated objects and part-level understanding. It connects visual perception of object structure to manipulation of joints, links, and contact-rich mechanisms.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Represent articulated assets

For a kinematic chain, link pose is $T_{WL}=T_{W0}\prod_iT_i(q_i)$. Revolute $q_i$ use radians; prismatic $q_i$ use meters. Joint axes, limits, and parent/child transforms are essential asset metadata.


**Component practice**

- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate an Articulated Object Schema — unreviewed idea; contract and evaluator required.
- Compute Joint-Conditioned Object State — unreviewed idea; contract and evaluator required.

### Render part-level observations

A part point maps to camera coordinates as $p_C=T_{CW}T_{WL}p_L$. RGB, depth, and part labels provide different information. Ground-truth part IDs or joint parameters are privileged annotations unless the learner contract includes them.



<!-- joint-tonic-math-expansion -->
#### Articulation changes the transform chain

For homogeneous part point $\widetilde p_L=[x,y,z,1]^\top$, use

$$\widetilde p_C=T_{CW}T_{WL}(q)\widetilde p_L,\qquad (u,v)=\left(f_x\frac{X_C}{Z_C}+c_x,\ f_y\frac{Y_C}{Z_C}+c_y\right).$$

$T_{WL}(q)$ maps articulated-link coordinates to world, $T_{CW}$ world to camera, translations are metres, and camera coordinates have +z forward. Intrinsics $f_x,f_y,c_x,c_y$ are pixels; projection requires $Z_C>0$ and the displayed equation assumes zero skew/distortion. Articulation q uses radians for hinges and metres for slides. A camera point $(0.1,0,1)$ metres with $f_x=500,c_x=320,c_y=240$ projects to $(370,240)$ pixels.

[Frame-graph transforms](/problems/trace-perception-frame-graph), [geometric Jacobians](/problems/geometric-jacobian-joint-axes), and [camera projection](/problems/project-camera-points) implement supporting geometry. They do not infer the hidden joint graph or reproduce SAPIEN's rendering/contact engine.
<!-- /joint-tonic-math-expansion -->

**Component practice**

- Supporting prerequisite: [Project Camera Points into Pixels](/problems/project-camera-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Project a Tracked Point Across Views — unreviewed idea; contract and evaluator required.

### Test interactive behavior

For target articulation $q^*$, a teaching completion error is $e=|q-q^*|$, with joint-specific units and tolerance. Endpoint error alone misses excessive force, collision, or wrong-part contact. Articulated asset diversity should be separated between training and held-out object instances.


**Component practice**

- Build a Reproducible Interaction Scenario — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).
- **Supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points).
- **Supporting prerequisite:** [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map).

**Planned component problems:**

- Validate an Articulated Object Schema — unreviewed idea; contract and evaluator required.
- Compute Joint-Conditioned Object State — unreviewed idea; contract and evaluator required.
- Project a Tracked Point Across Views — unreviewed idea; contract and evaluator required.
- Build a Reproducible Interaction Scenario — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Opening and manipulating household objects requires understanding movable parts. Incorrect axes or collision meshes can teach a policy interactions that are impossible on the real object.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2003.08515) · [Open-access manuscript](https://arxiv.org/pdf/2003.08515)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
