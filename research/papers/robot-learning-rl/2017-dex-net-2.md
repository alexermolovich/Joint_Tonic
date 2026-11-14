---
schema_version: 1
paper_id: "2017-dex-net-2"
title: "Dex-Net 2.0: Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics"
authors: ["Mahler, Jeffrey","Liang, Jacky","Niyaz, Sherdil","Laskey, Michael","Doan, Richard","Liu, Xinyu","Ojea, Juan Aparicio","Goldberg, Ken"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1703.09312"
pdf_url: "https://arxiv.org/pdf/1703.09312"
local_pdf: "./2017-dex-net-2.pdf"
sha256: "d61ceb68e54cf8496eed5c8bb76b783b59774d8a4e5ee914ff8db60f1f85f1a3"
bytes: 8096768
pages: 12
topics: ["robot-learning-rl","dex-net-2"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Generate robust grasp labels","detail":"Evaluate analytic grasp quality under uncertainty.","column":0,"row":0,"section":"Generate robust grasp labels","problem_slugs":[],"planned_problems":["Aggregate Analytic Grasp Quality Under Pose Perturbations"]},{"id":"stage-2","title":"Train a quality predictor","detail":"Map a grasp-aligned depth crop to success likelihood.","column":1,"row":0,"section":"Train a quality predictor","problem_slugs":[],"planned_problems":["Extract a Grasp-Aligned Depth Patch","Compute a Binary Grasp-Quality Loss"]},{"id":"stage-3","title":"Rank feasible candidates","detail":"Choose a high-quality grasp from sampled antipodal hypotheses.","column":2,"row":0,"section":"Rank feasible candidates","problem_slugs":[],"planned_problems":["Rank Grasp Candidates by Predicted Quality","Evaluate Grasp Precision Under a Safety Threshold"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"synthetic depth crops"},{"from":"stage-2","to":"stage-3","label":"quality scores"}]}
---

## Core paper explanation

Dex-Net 2.0 trains a grasp-quality CNN using synthetic depth observations and analytic robustness labels. At deployment, it samples parallel-jaw grasp candidates and ranks them from the observed depth image.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Generate robust grasp labels

For grasp $g$ and uncertain object/contact parameters $\xi$, expected quality is $Q(g)=\mathbb E_\xi[\epsilon(g,\xi)]$. Here $\epsilon$ is the analytic grasp metric, not diffusion noise. Sampling approximates robustness to pose, friction, and sensing uncertainty under the chosen model.


**Planned exercise:** Aggregate Analytic Grasp Quality Under Pose Perturbations.


### Train a quality predictor

For binary robust-grasp label $y$ and prediction $p_\theta$, training uses cross-entropy:
$$L=-y\log p_\theta-(1-y)\log(1-p_\theta).$$
The crop is aligned to the candidate grasp and conditioned on grasp depth. Camera geometry and gripper dimensions determine what the input means.


**Planned exercise:** Extract a Grasp-Aligned Depth Patch.

**Planned exercise:** Compute a Binary Grasp-Quality Loss.


### Rank feasible candidates

Select $g^*=\arg\max_{g\in\mathcal G}p_\theta(g\mid D)$ among candidates passing reachability and collision checks. A high analytic-quality prediction does not include every real contact or object-model error.


**Planned exercise:** Rank Grasp Candidates by Predicted Quality.

**Planned exercise:** Evaluate Grasp Precision Under a Safety Threshold.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Generate robust grasp labels:** Aggregate Analytic Grasp Quality Under Pose Perturbations (planned).
- **Train a quality predictor:** Extract a Grasp-Aligned Depth Patch (planned); Compute a Binary Grasp-Quality Loss (planned).
- **Rank feasible candidates:** Rank Grasp Candidates by Predicted Quality (planned); Evaluate Grasp Precision Under a Safety Threshold (planned).

## Why this matters on a robot

Synthetic labels reduce physical data collection, but friction uncertainty, missing depth, and gripper calibration can change real grasp success. Prediction confidence should be evaluated on physical trials.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1703.09312) · [Open-access manuscript](https://arxiv.org/pdf/1703.09312)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
