---
schema_version: 1
paper_id: "2024-paligemma"
title: "PaliGemma: A versatile 3B VLM for transfer"
authors: ["Beyer, Lucas","Steiner, Andreas","Pinto, André Susano","Kolesnikov, Alexander","Wang, Xiao","Salz, Daniel","Neumann, Maxim","Alabdulmohsin, Ibrahim","Tschannen, Michael","Bugliarello, Emanuele","Unterthiner, Thomas","Keysers, Daniel","Koppula, Skanda","Liu, Fangyu","Grycner, Adam","Gritsenko, Alexey","Houlsby, Neil","Kumar, Manoj","Rong, Keran","Eisenschlos, Julian","Kabra, Rishabh","Bauer, Matthias","Bošnjak, Matko","Chen, Xi","Minderer, Matthias","Voigtlaender, Paul","Bica, Ioana","Balazevic, Ivana","Puigcerver, Joan","Papalampidi, Pinelopi","Henaff, Olivier","Xiong, Xi","Soricut, Radu","Harmsen, Jeremiah","Zhai, Xiaohua"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2407.07726"
pdf_url: "https://arxiv.org/pdf/2407.07726"
local_pdf: "./2024-paligemma.pdf"
sha256: "aec6edd6b712597647d5e6e10850039d6415620163f45bb64f71d89718e6bb2f"
bytes: 3452867
pages: 59
topics: ["vlm-grounding","paligemma"]
modalities: ["rgb","text","spatial-tokens"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Build multimodal prefix","detail":"Project image tokens and append the task prompt.","column":0,"row":0,"section":"Build multimodal prefix","problem_slugs":[],"planned_problems":["Format Image-Prefix Language Sequences"]},{"id":"stage-2","title":"Apply prefix attention","detail":"Use full prefix visibility and causal suffix visibility.","column":1,"row":0,"section":"Apply prefix attention","problem_slugs":[],"planned_problems":["Build a Bidirectional-Prefix Causal-Suffix Attention Mask"]},{"id":"stage-3","title":"Train task suffixes","detail":"Supervise only the requested output sequence.","column":2,"row":0,"section":"Train task suffixes","problem_slugs":[],"planned_problems":["Encode Spatial Locations as Tokens","Validate Task-Specific Output Grammars"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"prefix and suffix"},{"from":"stage-2","to":"stage-3","label":"masked attention"}]}
---

## Core paper explanation

PaliGemma combines a SigLIP image encoder with a Gemma decoder-only language model for task-specific vision-language transfer. Its prefix attention and suffix-only training objective distinguish conditioning input from the sequence the model should generate.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Build multimodal prefix

Image tokens are projected into the language width and concatenated with prompt tokens. Let the prefix have length $P$ and the answer suffix length $T$. Image resolution controls the number of visual tokens and therefore the context budget.


**Planned component problems:** Format Image-Prefix Language Sequences. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Apply prefix attention

Ignoring padding, a teaching attention mask for query $i$ and key $j$ is
$$M_{ij}=\begin{cases}0&i<P,\ j<P,\\0&i\ge P,\ j\le i,\\-\infty&\text{otherwise}.\end{cases}$$
Prefix positions can see one another but cannot see answer tokens. Suffix positions can see the prefix and preceding suffix. Verify indexing against the actual implementation before batching.




**Planned component problem:** Build a Bidirectional-Prefix Causal-Suffix Attention Mask. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Train task suffixes

The loss is
$$L=-\sum_{t=1}^{T}\log p_\theta(y_t\mid y_{<t},I,x).$$
PaliGemma uses task-specific output formats, including normalized location tokens for detection and segmentation. Preserve task prompts, tokenizer, image resizing, and coordinate decoding as one versioned interface; transfer training is distinct from zero-shot chat use.


**Planned component problems:** Encode Spatial Locations as Tokens; Validate Task-Specific Output Grammars. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Compute Pairwise Bounding-Box IoU](/problems/box-iou-broadcast). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Format Image-Prefix Language Sequences.
- Build a Bidirectional-Prefix Causal-Suffix Attention Mask.
- Encode Spatial Locations as Tokens.
- Validate Task-Specific Output Grammars.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

A compact transferable VLM can specialize in robot-camera inspection. Prefix-mask leakage gives deceptively low training loss, while coordinate-order mistakes produce plausible but misplaced detections; test both interfaces independently.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2407.07726) · [Open-access manuscript](https://arxiv.org/pdf/2407.07726)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
