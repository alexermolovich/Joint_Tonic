---
schema_version: 1
paper_id: "2025-fast-action-tokenization"
title: "FAST: Efficient Action Tokenization for Vision-Language-Action Models"
authors: ["Pertsch, Karl","Stachowicz, Kyle","Ichter, Brian","Driess, Danny","Nair, Suraj","Vuong, Quan","Mees, Oier","Finn, Chelsea","Levine, Sergey"]
year: 2025
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2501.09747"
pdf_url: "https://arxiv.org/pdf/2501.09747"
local_pdf: "./2025-fast-action-tokenization.pdf"
sha256: "3739b31f5fecdde371509ff5bb13619979734e894a255a9b264253f4cc53934a"
bytes: 7468382
pages: 19
topics: ["vla-generalist","fast-action-tokenization"]
modalities: ["rgb","text","robot-state","actions"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Transform the action chunk","detail":"Apply a temporal discrete cosine transform per action channel.","column":0,"row":0,"section":"Transform the action chunk","problem_slugs":[],"planned_problems":["Transform an Action Chunk into Frequency Coefficients"]},{"id":"stage-2","title":"Quantize and compress","detail":"Flatten low-frequency coefficients first, then apply BPE.","column":1,"row":0,"section":"Quantize and compress","problem_slugs":[],"planned_problems":["Quantize Compressed Action Coefficients"]},{"id":"stage-3","title":"Decode a physical chunk","detail":"Invert BPE, dequantize, and apply the inverse transform.","column":2,"row":0,"section":"Decode a physical chunk","problem_slugs":[],"planned_problems":["Measure Codec Rate-Distortion Tradeoffs"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"DCT coefficients"},{"from":"stage-2","to":"stage-3","label":"generated action tokens"}]}
---
## Core paper explanation

FAST tokenizes an action chunk in frequency space, then compresses quantized coefficients with byte-pair encoding. This reduces the redundant token sequence produced by independently binning many highly correlated high-frequency actions.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Transform the action chunk

For normalized actions $A\in\mathbb R^{H\times d}$, an orthonormal DCT-II convention is
$$C_{kj}=\gamma_k\sum_{t=0}^{H-1}A_{tj}\cos\!\left[\frac\pi H(t+1/2)k\right],$$
with $\gamma_0=\sqrt{1/H}$ and $\gamma_k=\sqrt{2/H}$ for $k>0$. Match the tokenizer's normalization convention; low frequencies describe slow variation across the chunk.

<!-- joint-tonic-component:stage-1 -->
- **Planned component:** Transform an Action Chunk into Frequency Coefficients. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Quantize and compress

With precision scale $s>0$, coefficient quantization can be expressed as
$$Q_{kj}=\operatorname{round}(sC_{kj}).$$
FAST flattens coefficients with low-frequency components first across action dimensions, then learns BPE merges. Quantization is lossy; BPE is lossless relative to the integer coefficient sequence. The trained vocabulary and flattening order are part of the artifact.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Quantize Compressed Action Coefficients. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Decode a physical chunk

Reconstruction is $\hat A=\operatorname{IDCT}(Q/s)$. Under an orthonormal transform, $\|A-\hat A\|_F=\|C-Q/s\|_F$, making coefficient error interpretable. Restore per-channel physical scales afterward and reject malformed decoded lengths before commanding a robot.

<!-- joint-tonic-component:stage-3 -->
- **Planned component:** Measure Codec Rate-Distortion Tradeoffs. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.



Planned components: Transform an Action Chunk into Frequency Coefficients; Quantize Compressed Action Coefficients; Measure Codec Rate-Distortion Tradeoffs. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Compression can make autoregressive action learning more practical at high control frequencies. Smooth average reconstruction can hide brief contact-critical errors; evaluate peak channel errors and task success as well as token count.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2501.09747) · [Open-access manuscript](https://arxiv.org/pdf/2501.09747)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
