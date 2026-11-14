---
schema_version: 1
paper_id: "2021-maniskill"
title: "ManiSkill: Generalizable Manipulation Skill Benchmark with Large-Scale Demonstrations"
authors: ["Mu, Tongzhou","Ling, Zhan","Xiang, Fanbo","Yang, Derek","Li, Xuanlin","Tao, Stone","Huang, Zhiao","Jia, Zhiwei","Su, Hao"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2107.14483"
pdf_url: "https://arxiv.org/pdf/2107.14483"
local_pdf: "./2021-maniskill.pdf"
sha256: "90472755c9779e6088c8a94faaed0a4de3b9743d2d994c421973b0e7c402b374"
bytes: 14120364
pages: 24
topics: ["simulation-sim2real","maniskill"]
modalities: ["simulator-state","robot-actions","sensor-observations"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Sample an object instance","detail":"Choose a task and articulated asset with declared geometry.","column":0,"row":0,"section":"Sample an object instance","problem_slugs":[],"planned_problems":["Stratify Manipulation Object Instances"]},{"id":"stage-2","title":"Construct 3D observations","detail":"Transform visible depth into the policy point-cloud frame.","column":1,"row":0,"section":"Construct 3D observations","problem_slugs":["se3-transform-points","unproject-depth-map"],"planned_problems":["Validate Manipulation Task Observations"]},{"id":"stage-3","title":"Learn and test manipulation","detail":"Evaluate policies on held-out object geometries.","column":2,"row":0,"section":"Learn and test manipulation","problem_slugs":[],"planned_problems":["Normalize Action Bounds Across Tasks","Evaluate Skill Success Across Object Instances"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"camera observations"},{"from":"stage-2","to":"stage-3","label":"point clouds and demonstrations"}]}
---

## Core paper explanation

ManiSkill benchmarks manipulation across articulated objects with substantial geometric and topological variation. Point-cloud/RGB-D observations and demonstrations support studying generalizable perception and policy learning.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Sample an object instance

Split object identities into disjoint training and test sets. Reusing the same mesh with a new random seed tests state variation, not unseen-object generalization. Joint definitions and success predicates belong to the asset/task pair.


**Component practice**

- Stratify Manipulation Object Instances — unreviewed idea; contract and evaluator required.

### Construct 3D observations

For pixel homogeneous coordinate $\tilde u$ and depth $z$,
$$p_C=zK^{-1}\tilde u,\qquad p_B=T_{BC}p_C.$$
This pinhole formula requires axial depth and calibrated intrinsics; lens distortion or range-along-ray depth needs a different conversion. Declare whether policy points are camera-, base-, or world-frame.


**Component practice**

- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate Manipulation Task Observations — unreviewed idea; contract and evaluator required.

### Learn and test manipulation

Report success $\hat p_c$ per object category and instance, then state the weighting used for the aggregate. Equal episode weighting can overrepresent frequently sampled objects. Demonstration-based and interaction-based methods need comparable data/compute accounting.


**Component practice**

- Normalize Action Bounds Across Tasks — unreviewed idea; contract and evaluator required.
- Evaluate Skill Success Across Object Instances — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).
- **Supporting prerequisite:** [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map).

**Planned component problems:**

- Stratify Manipulation Object Instances — unreviewed idea; contract and evaluator required.
- Validate Manipulation Task Observations — unreviewed idea; contract and evaluator required.
- Normalize Action Bounds Across Tasks — unreviewed idea; contract and evaluator required.
- Evaluate Skill Success Across Object Instances — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Geometric variation tests whether a policy understands how objects move rather than memorizing one handle. Occluded joints and unseen articulation structure remain difficult even with accurate point clouds.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2107.14483) · [Open-access manuscript](https://arxiv.org/pdf/2107.14483)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
