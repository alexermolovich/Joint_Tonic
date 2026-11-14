---
schema_version: 1
paper_id: "2023-robocat"
title: "RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation"
authors: ["Bousmalis, Konstantinos","Vezzani, Giulia","Rao, Dushyant","Devin, Coline","Lee, Alex X.","Bauza, Maria","Davchev, Todor","Zhou, Yuxiang","Gupta, Agrim","Raju, Akhil","Laurens, Antoine","Fantacci, Claudio","Dalibard, Valentin","Zambelli, Martina","Martins, Murilo","Pevceviciute, Rugile","Blokzijl, Michiel","Denil, Misha","Batchelor, Nathan","Lampe, Thomas","Parisotto, Emilio","Żołna, Konrad","Reed, Scott","Colmenarejo, Sergio Gómez","Scholz, Jon","Abdolmaleki, Abbas","Groth, Oliver","Regli, Jean-Baptiste","Sushkov, Oleg","Rothörl, Tom","Chen, José Enrique","Aytar, Yusuf","Barker, Dave","Ortiz, Joy","Riedmiller, Martin","Springenberg, Jost Tobias","Hadsell, Raia","Nori, Francesco","Heess, Nicolas"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2306.11706"
pdf_url: "https://arxiv.org/pdf/2306.11706"
local_pdf: "./2023-robocat.pdf"
sha256: "ec66c1579baaada787820abf4ce99a9a59143b583ddcc6dfc4814623d1969831"
bytes: 26404959
pages: 60
topics: ["vla-generalist","robocat"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Encode visual goals","detail":"Tokenize observations and a desired future image.","column":0,"row":0,"section":"Encode visual goals","problem_slugs":[],"planned_problems":["Construct Goal-Conditioned Policy Batches"]},{"id":"stage-2","title":"Learn actions and future images","detail":"Jointly predict behavior and future visual tokens.","column":1,"row":0,"section":"Learn actions and future images","problem_slugs":[],"planned_problems":["Balance Robot-Task Training Mixtures"]},{"id":"stage-3","title":"Adapt and collect data","detail":"Fine-tune on a task, collect trajectories, then retrain the generalist.","column":2,"row":0,"section":"Adapt and collect data","problem_slugs":["validate-robot-episodes"],"planned_problems":["Track Adaptation Data Lineage"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"goal and observation tokens"},{"from":"stage-2","to":"stage-3","label":"generalist checkpoint"}]}
---
## Core paper explanation

RoboCat trains a goal-image-conditioned generalist manipulation policy and improves it through repeated adaptation and data collection. A VQ-GAN image tokenizer supports action prediction plus a future-image prediction auxiliary task.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Encode visual goals

A visual codebook maps image features $z$ to discrete entries:
$$q(z)=\arg\min_j\|z-e_j\|_2^2.$$
$e_j$ is codebook entry $j$; spatial code indices form an image sequence. A future image from an episode can act as a hindsight goal for earlier states, without requiring a verbal task label.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Construct Goal-Conditioned Policy Batches. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Learn actions and future images

A compact loss decomposition is
$$L=L_{\mathrm{action}}+L_{\mathrm{future\ image}},$$
where both terms are token negative log-likelihoods. The paper predicts images five timesteps ahead, avoiding an auxiliary task dominated by nearly unchanged consecutive frames. Context truncation and target masks must follow the training setup.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Balance Robot-Task Training Mixtures. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Adapt and collect data

The data loop can be written as $D_{r+1}=D_r\cup D_{\mathrm{new},r}$, followed by another generalist training stage. This set equation describes collection, not a guarantee of monotonically improving success. Preserve which policy collected each trajectory and how goals were relabeled.

<!-- joint-tonic-component:stage-3 -->
- **Related implementation prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).
- **Planned component:** Track Adaptation Data Lineage. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes)

Planned components: Construct Goal-Conditioned Policy Batches; Balance Robot-Task Training Mixtures; Track Adaptation Data Lineage. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Iterative collection can expand manipulation coverage across embodiments. A policy can also collect repetitive failures or exploit incorrect success labels; provenance and held-out task evaluation are essential to assess improvement.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2306.11706) · [Open-access manuscript](https://arxiv.org/pdf/2306.11706)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
