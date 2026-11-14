---
schema_version: 1
paper_id: "2022-code-as-policies"
title: "Code as Policies: Language Model Programs for Embodied Control"
authors: ["Liang, Jacky","Huang, Wenlong","Xia, Fei","Xu, Peng","Hausman, Karol","Ichter, Brian","Florence, Pete","Zeng, Andy"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2209.07753"
pdf_url: "https://arxiv.org/pdf/2209.07753"
local_pdf: "./2022-code-as-policies.pdf"
sha256: "e36857fa13746da031444ec59549e61204ca92d599b1d048ac1c55aaf1f6d0a3"
bytes: 3200561
pages: 16
topics: ["vla-generalist","code-as-policies"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Generate a policy program","detail":"Translate a task and API context into program tokens.","column":0,"row":0,"section":"Generate a policy program","problem_slugs":[],"planned_problems":["Validate a Restricted Robot Program AST"]},{"id":"stage-2","title":"Expand helper functions","detail":"Recursively define missing functions.","column":1,"row":0,"section":"Expand helper functions","problem_slugs":[],"planned_problems":["Trace a Composed Robot Policy"]},{"id":"stage-3","title":"Execute grounded operations","detail":"Call perception and motion primitives with live state.","column":2,"row":0,"section":"Execute grounded operations","problem_slugs":["se3-transform-points"],"planned_problems":["Resolve Perception Results into Control Calls"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"generated program"},{"from":"stage-2","to":"stage-3","label":"resolved functions"}]}
---
## Core paper explanation

Code as Policies uses language-model-generated programs to compose robot perception and control APIs. The generated policy can express geometry, branching, loops, and helper functions, rather than selecting only a single predefined skill.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Generate a policy program

For instruction $\ell$ and API context $c$, a code model represents
$$p(z\mid\ell,c)=\prod_t p(z_t\mid z_{<t},\ell,c),$$
where $z_t$ are program tokens. This describes code generation, not the probability that the resulting physical behavior is correct. Prompt examples establish available functions and argument conventions.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Validate a Restricted Robot Program AST. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Expand helper functions

Hierarchical generation detects undefined function calls and requests implementations. As a teaching dependency model, let $G=(F,E)$ have one node per function and edges for calls. Executability requires every reachable call to resolve to a generated definition or approved API. Recursive code generation is a construction strategy; it does not prove termination or safety.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Trace a Composed Robot Policy. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Execute grounded operations

A geometric instruction may compute $p^W=R_{WC}p^C+t_{WC}$ before calling a controller. Here points and translation are in meters and $R_{WC}$ maps camera-frame vectors into the world frame. Generated code must respect these API contracts. Run educational programs in isolation; real motion requires independent bounds and controller checks.

<!-- joint-tonic-component:stage-3 -->
- **Related implementation prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).
- **Planned component:** Resolve Perception Results into Control Calls. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points)

Planned components: Validate a Restricted Robot Program AST; Trace a Composed Robot Policy; Resolve Perception Results into Control Calls. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

The method makes compositional robot instructions explicit and inspectable. A syntactically valid program may use stale detections, wrong units, or a nonexistent object; logs should preserve generated code, API versions, observations, and command outcomes.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2209.07753) · [Open-access manuscript](https://arxiv.org/pdf/2209.07753)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
