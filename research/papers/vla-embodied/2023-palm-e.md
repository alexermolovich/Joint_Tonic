---
schema_version: 1
paper_id: "2023-palm-e"
title: "PaLM-E: An Embodied Multimodal Language Model"
authors:
  - "Danny Driess et al."
year: 2023
venue_or_status: "ICML 2023"
primary_url: "https://arxiv.org/abs/2303.03378"
pdf_url: "https://arxiv.org/pdf/2303.03378"
local_pdf: "./2023-palm-e.pdf"
sha256: "535cc3c7fe1ae7428b9ac7d6a3738a0529975aadc372b2229ea0cb2ce724576a"
bytes: 10707237
pages: 18
topics:
  - "embodied language model"
  - "multimodal tokens"
  - "robot planning"
  - "positive transfer"
modalities:
  - "text"
  - "RGB images"
  - "continuous state estimates"
track_role: "core"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Continuous observations become language-width embeddings, those embeddings are interleaved with text, and the language model predicts the requested output. Any downstream robot skill execution remains a separate interface.","nodes":[{"id":"stage-1","title":"Embed sensor evidence","detail":"Project visual or state features into the language model’s token width.","column":0,"row":0,"section":"Embed sensor evidence","problem_slugs":["palm-e-project-sensor-features"],"planned_problems":["Validate Missing-Modality and Stale-Sensor Inputs"]},{"id":"stage-2","title":"Interleave modalities and text","detail":"Construct an ordered sequence whose positions preserve observation context.","column":1,"row":0,"section":"Interleave modalities and text","problem_slugs":[],"planned_problems":["Interleave Image, State, and Text Tokens","Collate Variable Multimodal Sequences"]},{"id":"stage-3","title":"Generate the requested output","detail":"Predict language conditioned on the assembled embodied context.","column":2,"row":0,"section":"Generate the requested output","problem_slugs":[],"planned_problems":["Build a Multimodal Causal Attention Mask"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"sensor embeddings"},{"from":"stage-2","to":"stage-3","label":"multimodal sequence"}]}
---
## Core paper explanation

PaLM-E incorporates continuous visual and state information into a language model’s token sequence. Modality encoders transform observations into vectors of the language model’s embedding width, allowing sensor evidence and text to participate in one autoregressive reasoning process. Its robot-oriented use is embodied reasoning and planning; generating a textual plan is distinct from proving that every step is physically executable.

## Execution flow

Continuous observations become language-width embeddings, those embeddings are interleaved with text, and the language model predicts the requested output. Any downstream robot skill execution remains a separate interface.

### Embed sensor evidence

For modality $m$, an encoder $f_m$ and projection $P_m$ yield

$$
E_m=P_m(f_m(x_m))\in\mathbb R^{n_m\times d_{\mathrm{LM}}}.
$$

Here $n_m$ is that modality’s token count and $d_{\mathrm{LM}}$ is the language embedding width. The notation allows a learned projection, not necessarily one matrix multiplication. Original sensor units and frames belong to the input contract; the projected embedding coordinates no longer carry those physical units directly.

<!-- joint-tonic-component:stage-1 -->
- **Implement this component:** [Project Continuous Sensor Features into Language Width](/problems/palm-e-project-sensor-features).
- **Planned component:** Validate Missing-Modality and Stale-Sensor Inputs. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Interleave modalities and text

A multimodal prompt can be represented as

$$
E=[E_{\mathrm{text},1};E_{\mathrm{image}};E_{\mathrm{text},2};E_{\mathrm{state}};\ldots].
$$

Its total length is the sum of all inserted token counts. Position IDs, causal masks, and target-label positions must follow this assembled order. Dropping an image block without updating those arrays can train the model against the wrong output positions even though every tensor has a valid dtype.

<!-- joint-tonic-component:stage-2 -->
- **Planned component:** Interleave Image, State, and Text Tokens. This is an idea or blueprint, not a runnable exercise yet.
- **Planned component:** Collate Variable Multimodal Sequences. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

### Generate the requested output

For output tokens $y_1,\ldots,y_T$, teacher-forced training minimizes

$$
\mathcal L=-\sum_{i=1}^{T}\log p_\theta(y_i\mid E,y_{<i}).
$$

The target mask excludes prompt and sensor positions from output-token supervision. If the output is a plan, validate each proposed skill against the available skill library and current state. The probability of a sentence is not the probability that a controller can perform it.

<!-- joint-tonic-component:stage-3 -->
- **Planned component:** Build a Multimodal Causal Attention Mask. This is an idea or blueprint, not a runnable exercise yet.
<!-- /joint-tonic-component -->

## Implement the components

Runnable exercises are attached beside the relevant equations above and in the execution graph. Supporting prerequisites are labeled separately; a completed component does not reproduce the whole paper.

- [Project Continuous Sensor Features into Language Width](/problems/palm-e-project-sensor-features)

Planned components: Validate Missing-Modality and Stale-Sensor Inputs; Interleave Image, State, and Text Tokens; Collate Variable Multimodal Sequences; Build a Multimodal Causal Attention Mask. Exact approved curriculum titles are reused where available; additional named ideas require a reviewed blueprint before implementation.

[Browse the curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md).

## Why this matters on a robot

Interleaving enables questions and plans to depend on current observations, but stale frames and ambiguous references can corrupt reasoning. Keep observation timestamps and object identities available to the execution system. Evaluate plan grounding separately from language quality.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2303.03378) · [Open-access manuscript](https://arxiv.org/pdf/2303.03378)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
