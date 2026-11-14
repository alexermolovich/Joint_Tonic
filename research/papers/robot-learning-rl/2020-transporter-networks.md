---
schema_version: 1
paper_id: "2020-transporter-networks"
title: "Transporter Networks: Rearranging the Visual World for Robotic Manipulation"
authors: ["Zeng, Andy","Florence, Pete","Tompson, Jonathan","Welker, Stefan","Chien, Jonathan","Attarian, Maria","Armstrong, Travis","Krasin, Ivan","Duong, Dan","Wahid, Ayzaan","Sindhwani, Vikas","Lee, Johnny"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2010.14406"
pdf_url: "https://arxiv.org/pdf/2010.14406"
local_pdf: "./2020-transporter-networks.pdf"
sha256: "3a5e78b5c8881863845c46bda0bf8c9071aa79a59a6f9a9f4d8732690482b228"
bytes: 3781112
pages: 23
topics: ["robot-learning-rl","transporter-networks"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Build a spatial observation and pick map","detail":"Use a calibrated top-down representation to score grasp locations.","column":0,"row":0,"section":"Build a spatial observation and pick map","problem_slugs":[],"planned_problems":["Build a Pick Heatmap"]},{"id":"stage-2","title":"Transport pick features","detail":"Cross-correlate the selected object context with scene features.","column":1,"row":0,"section":"Transport pick features","problem_slugs":[],"planned_problems":["Correlate a Pick Feature Crop with a Place Map"]},{"id":"stage-3","title":"Train and execute spatial actions","detail":"Supervise demonstrated pick and placement locations.","column":2,"row":0,"section":"Train and execute spatial actions","problem_slugs":[],"planned_problems":["Decode a Spatial Action Distribution"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"pick location"},{"from":"stage-2","to":"stage-3","label":"placement scores"}]}
---

## Core paper explanation

Transporter Networks predict pick-and-place actions using spatial feature maps. A feature crop at the selected pick location is cross-correlated with the scene to find a compatible placement, preserving useful geometric structure.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Build a spatial observation and pick map

A fused RGB-D heightmap links image-grid cells to workspace positions. The pick network predicts a distribution $p_{\mathrm{pick}}(u\mid o)$. Cell size in meters and workspace bounds determine how a pixel action maps to the robot.


**Planned exercise:** Build a Pick Heatmap.


### Transport pick features

For pick-centered crop features $\psi$ and scene features $\phi$,
$$Q_{\mathrm{place}}(v)=\sum_{\delta,c}\psi(o[u+\delta])_c\,\phi(o[v+\delta])_c.$$
Rotated crop hypotheses extend the search over orientation. This is cross-correlation, so the kernel is not flipped as in mathematical convolution.


**Planned exercise:** Correlate a Pick Feature Crop with a Place Map.


### Train and execute spatial actions

A compact supervised loss is $L=-\log p_{\mathrm{pick}}(u^*)-\log p_{\mathrm{place}}(v^*\mid u^*)$. Pose extensions add additional action components. Calibration and motion planning turn spatial predictions into executable robot motion.


**Planned exercise:** Decode a Spatial Action Distribution.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Build a spatial observation and pick map:** Build a Pick Heatmap (planned).
- **Transport pick features:** Correlate a Pick Feature Crop with a Place Map (planned).
- **Train and execute spatial actions:** Decode a Spatial Action Distribution (planned).

## Why this matters on a robot

Spatial structure improves data efficiency for rearrangement. Heightmap occlusions, overlapping objects, and incorrect pixel-to-world calibration can still produce invalid grasps or placements.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2010.14406) · [Open-access manuscript](https://arxiv.org/pdf/2010.14406)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
