---
schema_version: 1
paper_id: "2024-openvla"
title: "OpenVLA: An Open-Source Vision-Language-Action Model"
authors:
  - "Moo Jin Kim et al."
year: 2024
venue_or_status: "CoRL 2024"
primary_url: "https://arxiv.org/abs/2406.09246"
pdf_url: "https://arxiv.org/pdf/2406.09246"
local_pdf: "./2024-openvla.pdf"
sha256: "353c37df34458f12f969b14dfd8b77175b727b9cddea7bb891759beddeefe1be"
bytes: 13240309
pages: 37
topics:
  - "open VLA"
  - "visual feature fusion"
  - "action tokenization"
  - "efficient fine-tuning"
modalities:
  - "RGB images"
  - "language instructions"
  - "discrete action tokens"
track_role: "advanced"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# OpenVLA: An Open-Source Vision-Language-Action Model

## Agent brief

OpenVLA is the best card for connecting model architecture to practical fine-tuning and serving. Teach feature fusion, dataset-derived action quantization, LoRA, quantization, and checkpoint/interface metadata. Avoid asking learners to train a 7B model from scratch.

## Contribution

- **Changed:** OpenVLA releases a large open vision-language-action model trained on diverse real-robot demonstrations. It combines complementary pretrained visual features with a language backbone, predicts tokenized actions, and studies memory-efficient fine-tuning and quantized deployment.
- **Evidence:** The reported evaluation is summarized below; the proposed exercises use deterministic small-scale proxies.
- **Not established:** The paper does not establish universal safety, unsupported-embodiment robustness, or equivalence of an educational reproduction.

## Prerequisite concepts

- Vision encoders and feature projection/fusion
- Decoder-only language models
- Quantile-based discretization
- LoRA, low-precision weights, and GPU memory accounting

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Visual backbones | Preprocessed RGB image | Complementary feature grids | Preprocessing version matches each backbone | Validate frozen feature extraction |
| Feature fusion | Two feature streams | LM-width visual tokens | Spatial/token alignment is explicit | Implement shape-safe fusion |
| VLM context builder | Visual and instruction tokens | Decoder context | Token order and masks are reproducible | Build multimodal collation |
| Quantile action codec | Training actions and new values | Bin edges, tokens, decoded actions | Edges fit training data only | Implement serializable quantile bins |
| Efficient tuner/serving | Base model and adapter/quantization config | Deployable checkpoint | Memory and tokenizer/schema versions are reported | Measure LoRA and quantized builds |

## Essential equations

For action component \(j\), training-set quantiles define edges

$$
b_{j,k}=Q_{A_j}\!\left(\frac{k}{B}\right),\quad k=1,\ldots,B-1,
\qquad
q_j(a)=\sum_{k=1}^{B-1}\mathbf 1[a>b_{j,k}].
$$

The action-token loss is categorical cross-entropy over the serialized target sequence:

$$
\mathcal L_{\text{token}}=-\sum_{t\in\mathcal T_{\text{action}}}\log p_\theta(\tau_t\mid I,c,\tau_{<t}),
$$

where \(I\) is the image input and \(c\) the instruction.

## Visual teaching plan

- **Feature-fusion diagram:** show two visual grids being aligned, concatenated/projected, and inserted before language tokens.
- **Quantile-bin explorer:** compare uniform and quantile bins on a skewed action histogram and inspect decode error.
- **Memory sandbox:** toggle dtype, LoRA rank, optimizer, and sequence length to update a component-wise GPU budget.

## Data and evaluation

- **Reported setting and protocol:** The model trains on a broad real-robot mixture and evaluates generalist manipulation, language grounding, multi-task adaptation, and efficient fine-tuning/serving choices. A scaled-down reproduction should measure quantization error, action-token accuracy, trainable memory, latency, and task success by environment.
- **Compute/hardware interpretation:** Reported scale and physical hardware materially affect comparability; do not infer equivalence from a toy run.
- **Educational boundary:** Use synthetic or licensed fixtures and report mechanism-level metrics separately from closed-loop outcomes.

## Limitations and failure modes

- A 7B model remains expensive for many edge-control targets.
- Quantile bins and action schemas are coupled to the training distribution.
- Visual feature fusion increases preprocessing and versioning complexity.
- Open weights do not remove upstream license or safety obligations.

## Implementation decomposition

1. Align two feature tensors by spatial/token layout.
2. Fuse and project them with explicit shape checks.
3. Fit action quantiles on training data only and serialize the codec.
4. Map action bins into a reserved token region.
5. Add LoRA to selected modules and report trainable memory.
6. Export a serving bundle with codec, preprocessing, and schema versions.

## Problem blueprints

### Problem: Fuse visual feature streams

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** two feature grids with documented shapes and projection weights
- **Outputs:** fused visual tokens at the language-model width
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** alignment, batch preservation, informative shape errors, gradient flow, deterministic output
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

### Problem: Fit and apply quantile action bins

- **Type:** pipeline
- **Difficulty:** medium
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** training actions, bin count, new action batch
- **Outputs:** monotonic bin edges, tokens, decoded centers
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** training-only fit, repeated quantile handling, clipping, serialization round trip, error bounds
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

### Problem: Estimate VLA deployment memory

- **Type:** optimization
- **Difficulty:** hard
- **Learning objective:** Implement and test this mechanism as an independent, observable skill.
- **Inputs:** parameter counts/dtypes, LoRA configuration, KV-cache shape, optimizer choice
- **Outputs:** component-wise train and inference memory budget
- **Fixture:** Deterministic synthetic or openly licensed data matching the declared interface.
- **Grading:** byte-accurate formulas, shared/frozen parameters, optimizer states, clear GiB units, ceiling comparison
- **Paper deviation:** Isolates one mechanism; omits the paper-scale model, data, and physical-robot experiment.

## MLOps and deployment extensions

- Treat visual preprocessors, backbone revisions, token mapping, bin edges, and action schema as one atomic model version. Record peak device memory and p95 latency on the deployment GPU. Add canary replays that compare action tokens and decoded commands across quantized and unquantized builds before promotion.

## Canonical sources

- [Primary landing page](https://arxiv.org/abs/2406.09246)
- [Open-access PDF](https://arxiv.org/pdf/2406.09246)
- [Official code or project page](https://openvla.github.io/)


