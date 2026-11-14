# VLA and Embodied Robotics Paper Set

Updated: 2026-11-13

## Scope and selection rationale

This is a curated implementation curriculum, not an exhaustive bibliography. The ten papers trace a useful engineering path from a scalable transformer policy (RT-1), through action-sequence models and embodied multimodal reasoning, to cross-robot data, open generalist policies, flow-matching VLAs, and a humanoid-oriented foundation model. Papers were selected when they offer at least one component that can be isolated into a deterministic coding exercise, an evaluation exercise, or a small end-to-end reproduction.

All local artifacts were downloaded from the paper's arXiv record. The landing-page links below are the canonical paper records; direct links resolve to the corresponding open-access PDFs.

## Papers and implementation-problem candidates

| Order | Paper | Authors | Year | Venue / status | Primary page | Direct PDF | Local PDF | Contribution | Candidate coding problems |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | RT-1: Robotics Transformer for Real-World Control at Scale | Anthony Brohan et al. | 2022 | RSS 2023 | [arXiv:2212.06817](https://arxiv.org/abs/2212.06817) | [PDF](https://arxiv.org/pdf/2212.06817) | [`2022-rt-1.pdf`](../papers/vla-embodied/2022-rt-1.pdf) | Introduces a scalable transformer policy that tokenizes robot actions and trains across a large, diverse set of real-robot tasks. | Tokenize and detokenize continuous actions with fixed bins; implement TokenLearner-style visual token selection; compute task-balanced trajectory sampling weights. |
| 2 | Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware | Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn | 2023 | RSS 2023 | [arXiv:2304.13705](https://arxiv.org/abs/2304.13705) | [PDF](https://arxiv.org/pdf/2304.13705) | [`2023-aloha-act.pdf`](../papers/vla-embodied/2023-aloha-act.pdf) | Introduces Action Chunking with Transformers (ACT) to predict temporally coherent bimanual action chunks from demonstrations. | Build sliding-window action chunks with padding masks; implement ACT's exponentially weighted temporal ensemble; compute a masked CVAE reconstruction-plus-KL loss. |
| 3 | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, Shuran Song | 2023 | RSS 2023; IJRR | [arXiv:2303.04137](https://arxiv.org/abs/2303.04137) | [PDF](https://arxiv.org/pdf/2303.04137) | [`2023-diffusion-policy.pdf`](../papers/vla-embodied/2023-diffusion-policy.pdf) | Frames visuomotor control as conditional action-sequence denoising with receding-horizon execution. | Implement forward diffusion and noise-prediction loss for action sequences; write a DDPM action sampler with conditioning; simulate receding-horizon execution and quantify inference latency. |
| 4 | PaLM-E: An Embodied Multimodal Language Model | Danny Driess et al. | 2023 | ICML 2023 | [arXiv:2303.03378](https://arxiv.org/abs/2303.03378) | [PDF](https://arxiv.org/pdf/2303.03378) | [`2023-palm-e.pdf`](../papers/vla-embodied/2023-palm-e.pdf) | Injects continuous sensor and vision embeddings into a language model for embodied reasoning, planning, and visual-language tasks. | Interleave projected image/state embeddings with text tokens; build multimodal causal attention masks; create a small embodied sequence-to-sequence batch collator. |
| 5 | RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control | Anthony Brohan et al. | 2023 | CoRL 2023 | [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) | [PDF](https://arxiv.org/pdf/2307.15818) | [`2023-rt-2.pdf`](../papers/vla-embodied/2023-rt-2.pdf) | Co-fine-tunes vision-language data and robot trajectories by representing actions as tokens in a shared autoregressive output space. | Serialize and parse robot actions as discrete text tokens; mix web/VQA and robot batches at a target ratio; enforce grammar-constrained action-token decoding. |
| 6 | Open X-Embodiment: Robotic Learning Datasets and RT-X Models | Open X-Embodiment Collaboration, Abby O'Neill et al. | 2023 | ICRA 2024 | [arXiv:2310.08864](https://arxiv.org/abs/2310.08864) | [PDF](https://arxiv.org/pdf/2310.08864) | [`2023-open-x-embodiment.pdf`](../papers/vla-embodied/2023-open-x-embodiment.pdf) | Standardizes heterogeneous robot datasets and demonstrates positive transfer from cross-embodiment RT-X training. | Normalize robot-specific observations/actions into a shared trajectory schema; implement per-dataset weighted sampling; mask unavailable action dimensions in a cross-embodiment loss. |
| 7 | Octo: An Open-Source Generalist Robot Policy | Octo Model Team, Dibya Ghosh et al. | 2024 | RSS 2024 | [arXiv:2405.12213](https://arxiv.org/abs/2405.12213) | [PDF](https://arxiv.org/pdf/2405.12213) | [`2024-octo.pdf`](../papers/vla-embodied/2024-octo.pdf) | Provides an open transformer policy pretrained on Open X-Embodiment and designed to adapt to new sensors, action spaces, and goals. | Assemble Octo-style observation/task token groups and masks; implement dataset-specific action heads; add a frozen-backbone adapter and verify trainable-parameter counts. |
| 8 | OpenVLA: An Open-Source Vision-Language-Action Model | Moo Jin Kim et al. | 2024 | CoRL 2024 | [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) | [PDF](https://arxiv.org/pdf/2406.09246) | [`2024-openvla.pdf`](../papers/vla-embodied/2024-openvla.pdf) | Releases a 7B VLA with fused pretrained visual features, action-token prediction, and efficient fine-tuning and serving recipes. | Fuse two visual feature streams with shape-safe projection; implement action quantization using training-set quantiles; calculate LoRA parameter/memory savings and quantized serving budgets. |
| 9 | $\pi_0$: A Vision-Language-Action Flow Model for General Robot Control | Kevin Black et al. | 2024 | arXiv 2024; RSS 2025 | [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) | [PDF](https://arxiv.org/pdf/2410.24164) | [`2024-pi0.pdf`](../papers/vla-embodied/2024-pi0.pdf) | Couples a pretrained vision-language backbone to a flow-matching action expert for dexterous, cross-embodiment robot control. | Sample flow-matching interpolation states and targets; implement Euler integration for action generation; construct block attention masks between VLM and action-expert tokens. |
| 10 | GR00T N1: An Open Foundation Model for Generalist Humanoid Robots | NVIDIA, Johan Bjorck et al. | 2025 | arXiv technical report | [arXiv:2503.14734](https://arxiv.org/abs/2503.14734) | [PDF](https://arxiv.org/pdf/2503.14734) | [`2025-gr00t-n1.pdf`](../papers/vla-embodied/2025-gr00t-n1.pdf) | Combines a vision-language reasoning system with a diffusion-transformer action system trained with flow matching on real, human-video, and synthetic data. | Route multimodal inputs through a dual-system interface; implement a masked action flow-matching loss; build a heterogeneous batch sampler with source-ratio and embodiment metrics. |

## Companion agent paper cards

Every PDF has a same-basename Markdown card beside it. Cards are original teaching summaries rather than transcriptions. Each includes normalized YAML metadata, 1-3 essential equations where appropriate, a visual teaching plan, an implementation decomposition, executable problem blueprints with grading contracts, deployment/MLOps extensions, and canonical source links.

| PDF | Agent paper card |
| --- | --- |
| [`2022-rt-1.pdf`](../papers/vla-embodied/2022-rt-1.pdf) | [`2022-rt-1.md`](../papers/vla-embodied/2022-rt-1.md) |
| [`2023-aloha-act.pdf`](../papers/vla-embodied/2023-aloha-act.pdf) | [`2023-aloha-act.md`](../papers/vla-embodied/2023-aloha-act.md) |
| [`2023-diffusion-policy.pdf`](../papers/vla-embodied/2023-diffusion-policy.pdf) | [`2023-diffusion-policy.md`](../papers/vla-embodied/2023-diffusion-policy.md) |
| [`2023-open-x-embodiment.pdf`](../papers/vla-embodied/2023-open-x-embodiment.pdf) | [`2023-open-x-embodiment.md`](../papers/vla-embodied/2023-open-x-embodiment.md) |
| [`2023-palm-e.pdf`](../papers/vla-embodied/2023-palm-e.pdf) | [`2023-palm-e.md`](../papers/vla-embodied/2023-palm-e.md) |
| [`2023-rt-2.pdf`](../papers/vla-embodied/2023-rt-2.pdf) | [`2023-rt-2.md`](../papers/vla-embodied/2023-rt-2.md) |
| [`2024-octo.pdf`](../papers/vla-embodied/2024-octo.pdf) | [`2024-octo.md`](../papers/vla-embodied/2024-octo.md) |
| [`2024-openvla.pdf`](../papers/vla-embodied/2024-openvla.pdf) | [`2024-openvla.md`](../papers/vla-embodied/2024-openvla.md) |
| [`2024-pi0.pdf`](../papers/vla-embodied/2024-pi0.pdf) | [`2024-pi0.md`](../papers/vla-embodied/2024-pi0.md) |
| [`2025-gr00t-n1.pdf`](../papers/vla-embodied/2025-gr00t-n1.pdf) | [`2025-gr00t-n1.md`](../papers/vla-embodied/2025-gr00t-n1.md) |

## Suggested prerequisite and track order

1. **Shared foundations:** NumPy/PyTorch tensor shapes, transformers and causal masks, behavior cloning, coordinate frames, and trajectory datasets.
2. **Policy mechanics:** RT-1, ACT, then Diffusion Policy. These yield compact exercises in action representation, sequence prediction, and closed-loop execution.
3. **Language and semantic grounding:** PaLM-E, then RT-2. Learners move from multimodal token construction to action-as-language training.
4. **Data engineering and transfer:** Open X-Embodiment, then Octo. This is the strongest bridge to dataset versioning, schema validation, sampling, and adaptation-oriented MLOps problems.
5. **Open VLA implementation:** OpenVLA, then $\pi_0$. These expose practical fine-tuning/serving tradeoffs and two major action-generation families: discrete tokens and continuous flow matching.
6. **Humanoid integration:** GR00T N1. Treat it as a capstone joining heterogeneous data, a dual-system architecture, action flow matching, and deployment constraints.

## Artifact validation

Validation was performed on 2026-11-13. Every file begins with the ASCII `%PDF-` signature, and Poppler `pdfinfo` successfully parsed every document.

| File | Bytes | Pages | SHA-256 |
| --- | ---: | ---: | --- |
| `2022-rt-1.pdf` | 14,672,588 | 31 | `81efe669c8fa50ffc7097886dc78a442fa7a8f7f2451684b93069cb9fbeda767` |
| `2023-aloha-act.pdf` | 5,353,485 | 18 | `2e2fe25860f5f9cee9e655a2714e9f2264a7a5078bcd267c16d3f39af461345a` |
| `2023-diffusion-policy.pdf` | 6,192,199 | 19 | `b65c474b696a4802d8f1457d86b637ce2c5521412570d3aa928cd54563babc8f` |
| `2023-open-x-embodiment.pdf` | 4,011,306 | 12 | `13f16aff5afdee583dc25b3c570e9bb0cf6baefb59b539928d919588cd8d9246` |
| `2023-palm-e.pdf` | 10,707,237 | 18 | `535cc3c7fe1ae7428b9ac7d6a3738a0529975aadc372b2229ea0cb2ce724576a` |
| `2023-rt-2.pdf` | 15,668,163 | 26 | `0a62dc36bbbfdea232ad45a0ab75c82e9cf535b55333ff22c02d5da1897ccac3` |
| `2024-octo.pdf` | 3,675,649 | 17 | `73bff297cfafe523319162124e6b7f96919c0930e0a380f307255c4c7464ac93` |
| `2024-openvla.pdf` | 13,240,309 | 37 | `353c37df34458f12f969b14dfd8b77175b727b9cddea7bb891759beddeefe1be` |
| `2024-pi0.pdf` | 7,893,845 | 17 | `fbdfba56258bdbd220207ba63410c6c943e43a73e97a7a5a47ca0bc74204f821` |
| `2025-gr00t-n1.pdf` | 21,021,950 | 36 | `76e38cf679637b816b16edf7170340883dd09175bf334aeeaed49392777731b9` |

## Important product boundary

The papers are source material, not permission to copy their prose, diagrams, or code. Joint Tonic problems should use original explanations, independently written starter code and tests, and short attributed quotations only when essential. Link back to the canonical paper and respect each linked code repository's license separately.
