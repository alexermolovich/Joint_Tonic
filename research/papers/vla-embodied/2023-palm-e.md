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
---

# PaLM-E: An Embodied Multimodal Language Model

## Agent brief

Use PaLM-E to teach multimodal sequence assembly, not large-model replication. A good exercise projects continuous observations into the language-model embedding width, interleaves them with text tokens, and constructs labels/masks that train only the intended outputs.

## Contribution

- **Changed:** PaLM-E treats images and continuous sensor estimates as learned embeddings inserted into a language-model sequence. Joint training across embodied tasks and general vision-language/language data shows how a single model can reason about robot plans while retaining broad semantic capabilities.
- **Evidence:** The reported evaluation is summarized below; the proposed exercises use deterministic small-scale proxies.
- **Not established:** The paper does not establish universal safety, unsupported-embodiment robustness, or equivalence of an educational reproduction.

## Prerequisite concepts

- Token embeddings and causal language modeling
- Vision encoders and projection layers
- Multitask batching and loss masking
- Embodied planning versus low-level control

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Modality encoder | Image or robot state | Continuous features | Modality-specific order is stable | Validate feature shapes and batching |
| Projection | Modality features | LM-width embeddings | Final width equals `d_model` | Implement a typed projection registry |
| Sequence composer | Text and sensor embeddings | Interleaved sequence | Placeholder order and counts agree | Build multimodal collation |
| Causal model | Interleaved embeddings and masks | Next-token distributions | Prompt/sensor positions are excluded from loss | Construct causal and label masks |
| Plan validator | Generated plan and world schema | Validity and first failure | Only allowlisted grounded actions pass | Implement symbolic preconditions |

## Essential equations

For modality encoder \(f_m\) and learned projection \(P_m\), an embodied observation becomes language-width embeddings

$$
E_m(x)=P_m f_m(x)\in\mathbb R^{n_m\times d_{\text{LM}}}.
$$

After interleaving sensor and text embeddings into \(E=(e_1,\ldots,e_n)\), causal generation uses

$$
\mathcal L_{\text{gen}}=-\sum_{i\in\mathcal T_{\text{target}}}\log p_\theta(y_i\mid E,y_{<i}),
$$

where prompt and sensor positions are excluded from \(\mathcal T_{\text{target}}\).

## Visual teaching plan

- **Sequence composer:** drag image/state/text blocks into a prompt and inspect token positions, modality IDs, and loss masks.
- **Projection view:** compare source feature width with LM width and show how multiple visual tokens expand context length.
- **Plan checker:** animate a generated symbolic plan and stop at the first violated precondition.

## Data and evaluation

- **Reported setting and protocol:** The paper jointly evaluates embodied planning/manipulation, visual question answering, captioning, and language tasks, with attention to transfer across tasks and model scales. A compact reproduction should measure sequence correctness, modality ablations, mask correctness, and transfer between two small task families.
- **Compute/hardware interpretation:** Reported scale and physical hardware materially affect comparability; do not infer equivalence from a toy run.
- **Educational boundary:** Use synthetic or licensed fixtures and report mechanism-level metrics separately from closed-loop outcomes.

## Limitations and failure modes

- High-level text generation does not itself guarantee safe executable control.
- Large-scale gains are expensive to reproduce and may depend on unavailable data.
- Sensor-token alignment and truncation policies can silently remove crucial context.
- Fluent plans can be physically invalid or ungrounded.

## Implementation decomposition

1. Define typed placeholders for each non-text modality.
2. Encode and project each observation into one or more embeddings.
3. Replace placeholders without changing intended token order.
4. Build causal attention, padding, and loss masks.
5. Add task IDs and weighted multitask losses.
6. Validate generated plans with a separate symbolic or simulator checker.

## Problem blueprints

### Problem: Interleave multimodal embeddings

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** text embeddings, placeholder positions, per-example sensor embeddings
- **Outputs:** combined embeddings, attention mask, modality map
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** stable order, variable counts, padding behavior, gradient flow, shape validation
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

### Problem: Build labels for embodied generation

- **Type:** pipeline
- **Difficulty:** medium
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** multimodal prompt segments and target text
- **Outputs:** input IDs/embeddings, causal mask, labels with ignored prompt positions
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** no target leakage, correct ignore index, truncation policy, batched padding
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

### Problem: Validate a generated robot plan

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** generated action strings, object/state schema, preconditions/effects
- **Outputs:** validity result and first failing step
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** parser robustness, precondition updates, unknown-object handling, precise diagnostics
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

## MLOps and deployment extensions

- Version the tokenizer, placeholder vocabulary, modality encoders, and projection shapes together. Log truncation rates per modality and task. Before sending a generated plan to hardware, require schema validation, feasibility checks, and an allowlisted action compiler; language-model confidence is not a safety gate.

## Canonical sources

- [Primary landing page](https://arxiv.org/abs/2303.03378)
- [Open-access PDF](https://arxiv.org/pdf/2303.03378)
- [Official code or project page](https://palm-e.github.io/)


