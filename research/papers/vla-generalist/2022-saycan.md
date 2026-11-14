---
schema_version: 1
paper_id: "2022-saycan"
title: "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances"
authors: ["Ahn, Michael","Brohan, Anthony","Brown, Noah","Chebotar, Yevgen","Cortes, Omar","David, Byron","Finn, Chelsea","Fu, Chuyuan","Gopalakrishnan, Keerthana","Hausman, Karol","Herzog, Alex","Ho, Daniel","Hsu, Jasmine","Ibarz, Julian","Ichter, Brian","Irpan, Alex","Jang, Eric","Ruano, Rosario Jauregui","Jeffrey, Kyle","Jesmonth, Sally","Joshi, Nikhil J","Julian, Ryan","Kalashnikov, Dmitry","Kuang, Yuheng","Lee, Kuang-Huei","Levine, Sergey","Lu, Yao","Luu, Linda","Parada, Carolina","Pastor, Peter","Quiambao, Jornell","Rao, Kanishka","Rettinghouse, Jarek","Reyes, Diego","Sermanet, Pierre","Sievers, Nicolas","Tan, Clayton","Toshev, Alexander","Vanhoucke, Vincent","Xia, Fei","Xiao, Ted","Xu, Peng","Xu, Sichun","Yan, Mengyuan","Zeng, Andy"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2204.01691"
pdf_url: "https://arxiv.org/pdf/2204.01691"
local_pdf: "./2022-saycan.pdf"
sha256: "48c22d36a044bbbd34e640beb1db4fb4ba57e74d97fefa0fb121d55c31282312"
bytes: 12827088
pages: 34
topics: ["vla-generalist","saycan"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Score task relevance","detail":"Evaluate candidate skill descriptions in context.","column":0,"row":0,"section":"Score task relevance","problem_slugs":[],"planned_problems":["Score Task Relevance for Available Robot Skills"]},{"id":"stage-2","title":"Ground with feasibility","detail":"Combine language likelihood and learned skill value.","column":1,"row":0,"section":"Ground with feasibility","problem_slugs":[],"planned_problems":["Combine Skill Likelihood and Feasibility Scores","Rank Grounded Skill Candidates"]},{"id":"stage-3","title":"Execute and replan","detail":"Run one skill, observe the new state, then choose again.","column":2,"row":0,"section":"Execute and replan","problem_slugs":[],"planned_problems":["Stop a Skill Sequence at Completion"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"candidate skills"},{"from":"stage-2","to":"stage-3","label":"selected skill"}]}
---
## Core paper explanation

SayCan grounds language-based planning in a library of executable robot skills. A language model scores how useful a skill is for an instruction, while a learned affordance/value function scores whether that skill is achievable from the current state.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Score task relevance

For instruction $\ell$, executed history $h$, and candidate skill description $d_k$, the language score is $P_{\mathrm{LM}}(d_k\mid\ell,h)$. The candidate set is limited to skills the robot can actually execute; free-form text is not automatically a new skill.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Score Task Relevance for Available Robot Skills. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Ground with feasibility

Let $V_k(s)$ estimate success of skill $k$ in state $s$. SayCan selects using the product
$$k^*=\arg\max_k P_{\mathrm{LM}}(d_k\mid\ell,h)V_k(s).$$
Numerically, compare $\log P_{\mathrm{LM}}+\log V_k$ with explicit handling of zero values. This factorization is a modeling assumption; an uncalibrated value estimate does not become a guaranteed success probability.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Combine Skill Likelihood and Feasibility Scores. This is an idea or blueprint, not a runnable exercise yet.
- **Planned component:** Rank Grounded Skill Candidates. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Execute and replan

The control loop is $s_{t+1}\sim P(\cdot\mid s_t,\pi_{k_t})$, followed by a new skill selection with updated history. $\pi_k$ is the learned low-level skill policy, not the language model. Termination must be represented in the candidate plan and checked against task completion.

<!-- joint-tonic-component:stage-3 -->
- **Planned component:** Stop a Skill Sequence at Completion. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.



Planned components: Score Task Relevance for Available Robot Skills; Combine Skill Likelihood and Feasibility Scores; Rank Grounded Skill Candidates; Stop a Skill Sequence at Completion. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Language priors can propose sensible long-horizon behavior while affordances rule out currently infeasible steps. A skill library with no recovery behavior or inaccurate value estimates can still produce repeated failures.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2204.01691) · [Open-access manuscript](https://arxiv.org/pdf/2204.01691)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
