# Vision, VLM, and 3D Perception Paper Set

This is a curated implementation curriculum for physical-AI perception, not a claim to cover every important paper. The set deliberately connects real-time 2D detection, transformer backbones and set prediction, vision-language supervision, promptable perception, reusable visual features, point-cloud processing, and multi-view scene representations. Every paper is available from an official open-access source and has a validated local PDF.

Each PDF has a same-basename Markdown paper card beside it in `../papers/vision-vlm-3d/`. These sidecars provide machine-readable provenance, an original agent brief, verified essential equations, theory-page visual plans, practical executable problem blueprints, and MLOps/deployment extensions. Agents should use the card as an index and the canonical source links/PDF for verification rather than treating the card as a substitute citation.

## Why these papers

- **Detection:** YOLO v1 establishes single-stage real-time detection; DETR provides the contrasting set-prediction formulation; Grounding DINO extends detection to language-specified, open-set objects.
- **Backbones and representations:** ViT supplies the patch-token backbone used throughout modern vision, while CLIP and DINOv2 cover language-supervised and self-supervised reusable representations.
- **Segmentation:** SAM makes prompting, cached image embeddings, and a lightweight mask decoder concrete implementation targets.
- **3D and multi-view:** PointNet covers unordered geometric inputs, NeRF covers differentiable volume rendering, and BEVFormer covers calibrated multi-camera and temporal fusion for autonomy.
- **Physical-AI fit:** Together, these papers support problems on sensing, grounding, localization, geometry, latency, and deployment-facing evaluation rather than image classification alone.

## Selected papers and implementation ideas

| Paper | Year | Authors | Venue / status | Primary landing page | Direct PDF | Local PDF | Contribution | Candidate coding problems |
|---|---:|---|---|---|---|---|---|---|
| You Only Look Once: Unified, Real-Time Object Detection | 2016 | Joseph Redmon; Santosh Divvala; Ross Girshick; Ali Farhadi | CVPR 2016 | [arXiv:1506.02640](https://arxiv.org/abs/1506.02640) | [PDF](https://arxiv.org/pdf/1506.02640) | [`2016-yolo-v1.pdf`](../papers/vision-vlm-3d/2016-yolo-v1.pdf) | Reframes detection as one end-to-end regression pass over a fixed grid, making the accuracy/latency tradeoff explicit. | Decode grid-cell predictions into image boxes; compute YOLO v1 responsibility masks and loss terms; implement class-aware NMS and mAP evaluation. |
| PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation | 2017 | Charles R. Qi; Hao Su; Kaichun Mo; Leonidas J. Guibas | CVPR 2017 | [arXiv:1612.00593](https://arxiv.org/abs/1612.00593) | [PDF](https://arxiv.org/pdf/1612.00593) | [`2017-pointnet.pdf`](../papers/vision-vlm-3d/2017-pointnet.pdf) | Directly processes unordered point sets using shared per-point transformations and a symmetric aggregation function. | Prove/test permutation invariance with max pooling; implement a shared point MLP plus global feature; compute segmentation features by concatenating local and global descriptors. |
| End-to-End Object Detection with Transformers (DETR) | 2020 | Nicolas Carion; Francisco Massa; Gabriel Synnaeve; Nicolas Usunier; Alexander Kirillov; Sergey Zagoruyko | ECCV 2020 | [arXiv:2005.12872](https://arxiv.org/abs/2005.12872) | [PDF](https://arxiv.org/pdf/2005.12872) | [`2020-detr.pdf`](../papers/vision-vlm-3d/2020-detr.pdf) | Casts detection as direct set prediction with learned queries, bipartite matching, and no anchor generation or NMS. | Implement Hungarian matching cost; compute matched classification/L1/GIoU losses including no-object targets; decode normalized center-format predictions. |
| NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis | 2020 | Ben Mildenhall; Pratul P. Srinivasan; Matthew Tancik; Jonathan T. Barron; Ravi Ramamoorthi; Ren Ng | ECCV 2020 oral | [arXiv:2003.08934](https://arxiv.org/abs/2003.08934) | [PDF](https://arxiv.org/pdf/2003.08934) | [`2020-nerf.pdf`](../papers/vision-vlm-3d/2020-nerf.pdf) | Represents a scene as a continuous radiance/density field trained through differentiable volume rendering from posed images. | Generate stratified samples along calibrated camera rays; implement alpha compositing/transmittance weights; encode 3D coordinates with sinusoidal positional features. |
| An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale | 2021 | Alexey Dosovitskiy et al. (12 authors) | ICLR 2021 | [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) | [PDF](https://arxiv.org/pdf/2010.11929) | [`2021-vision-transformer.pdf`](../papers/vision-vlm-3d/2021-vision-transformer.pdf) | Turns an image into a sequence of learned patch tokens and applies a standard Transformer encoder. | Implement patchify/unpatchify with strict shape checks; interpolate learned position embeddings for a new resolution; assemble a pre-norm ViT encoder block. |
| Learning Transferable Visual Models From Natural Language Supervision (CLIP) | 2021 | Alec Radford et al. (12 authors) | ICML 2021 | [arXiv:2103.00020](https://arxiv.org/abs/2103.00020) | [PDF](https://arxiv.org/pdf/2103.00020) | [`2021-clip.pdf`](../papers/vision-vlm-3d/2021-clip.pdf) | Learns aligned image/text representations at scale with a symmetric contrastive objective and enables zero-shot classification by prompting. | Implement the symmetric image-to-text/text-to-image loss; build a zero-shot classifier from prompt ensembles; calculate retrieval recall@K from normalized embeddings. |
| BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers | 2022 | Zhiqi Li; Wenhai Wang; Hongyang Li; Enze Xie; Chonghao Sima; Tong Lu; Qiao Yu; Jifeng Dai | ECCV 2022 | [arXiv:2203.17270](https://arxiv.org/abs/2203.17270) | [PDF](https://arxiv.org/pdf/2203.17270) | [`2022-bevformer.pdf`](../papers/vision-vlm-3d/2022-bevformer.pdf) | Builds a unified bird's-eye-view representation from calibrated cameras using spatial cross-attention and temporal self-attention. | Project BEV reference points into each camera with validity masks; warp a prior BEV using ego motion; aggregate multi-camera sampled features with attention weights. |
| Segment Anything | 2023 | Alexander Kirillov et al. (12 authors) | ICCV 2023 | [arXiv:2304.02643](https://arxiv.org/abs/2304.02643) | [PDF](https://arxiv.org/pdf/2304.02643) | [`2023-segment-anything.pdf`](../papers/vision-vlm-3d/2023-segment-anything.pdf) | Introduces promptable segmentation, a reusable image embedding plus prompt/mask decoders, and a large-scale mask data engine. | Encode positive/negative point prompts and box corners; select masks using predicted IoU; implement stability-score filtering and mask NMS for automatic mask generation. |
| Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection | 2023 | Shilong Liu et al. (12 authors) | ECCV 2024 | [arXiv:2303.05499](https://arxiv.org/abs/2303.05499) | [PDF](https://arxiv.org/pdf/2303.05499) | [`2023-grounding-dino.pdf`](../papers/vision-vlm-3d/2023-grounding-dino.pdf) | Adds tight vision-language fusion, language-guided query selection, and cross-modal decoding to open-set object detection. | Construct a token-positive map for phrase grounding; select top queries from text-conditioned encoder scores; post-process token logits into phrase-labeled boxes. |
| DINOv2: Learning Robust Visual Features without Supervision | 2023 | Maxime Oquab et al. (26 authors) | TMLR 2024 | [arXiv:2304.07193](https://arxiv.org/abs/2304.07193) | [PDF](https://arxiv.org/pdf/2304.07193) | [`2023-dinov2.pdf`](../papers/vision-vlm-3d/2023-dinov2.pdf) | Scales self-supervised ViT training, curated data, distillation, and patch-level objectives into robust general-purpose visual features. | Implement teacher-temperature centering and EMA update; combine class-token and masked-patch losses; evaluate frozen patch features with a k-NN classifier. |

## Recommended learning order

1. **Image and box mechanics:** YOLO v1 - grid assignment, box transforms, IoU, NMS, and detection metrics.
2. **Tokenized vision:** ViT - patch embeddings, positional information, attention, and pre-norm blocks.
3. **Set prediction:** DETR - object queries, Hungarian assignment, and set losses.
4. **Reusable semantic features:** CLIP, then DINOv2 - contrastive alignment, self-distillation, and frozen-feature evaluation.
5. **Promptable/open-world perception:** SAM, then Grounding DINO - geometric prompts, masks, phrase grounding, and cross-modal query selection.
6. **3D geometry:** PointNet, then NeRF - unordered sets, calibrated rays, and differentiable rendering.
7. **Robot/autonomy scene fusion:** BEVFormer - camera calibration, multi-view sampling, ego-motion alignment, and temporal aggregation.

Cross-cutting prerequisites are NumPy/PyTorch tensor semantics, convolution and attention basics, probability and cross-entropy, coordinate systems and homogeneous transforms, and standard detection metrics. The 3D track additionally assumes pinhole-camera projection and rigid transforms.

## Local file validation

Validation was performed after download. Every file begins with the `%PDF-` signature and can be parsed by Poppler's `pdfinfo`.

| Local file | Bytes | Pages | SHA-256 |
|---|---:|---:|---|
| `2016-yolo-v1.pdf` | 5,296,750 | 10 | `54bcd2dd05dc618849e8a94d8b88fe3eeb37f80e96e200600d38f1f733931678` |
| `2017-pointnet.pdf` | 9,083,131 | 19 | `f13e3b3c744a3977155876e2d5dcd1d0cf83c22f98ce9cc11e0a2f5e37388b6a` |
| `2020-detr.pdf` | 7,634,041 | 26 | `d4b846bd44896e1d21527f48eddc422c263c9a4f8a3fa4be249750956882698d` |
| `2020-nerf.pdf` | 8,274,228 | 25 | `c7fc70b38f84cb2e42890a69a7c9b9c26ded464b221e0355031004f24fb8e727` |
| `2021-clip.pdf` | 6,813,639 | 48 | `6478b6e571a7d6fcd846d8ef77bfd60c285f1986abb8f475eedc43de403074f5` |
| `2021-vision-transformer.pdf` | 3,743,814 | 22 | `8ce7b83971a14508ca711a27c875c9b6914c4f6767cf3150fb1ca6c07aa056d6` |
| `2022-bevformer.pdf` | 4,739,748 | 20 | `641561d0e4c1d46d6883a3d38c68b475030de5bbbcdf747af268366f47f97a6b` |
| `2023-grounding-dino.pdf` | 4,329,735 | 33 | `ba1c64ec2ac4fedeb50b269eadc994456a8428dbe64a8dba2673f22df0fa20b3` |
| `2023-segment-anything.pdf` | 15,644,599 | 30 | `c6ca524e47200c3e542587ca76ac1dbc89cc67340f948c819250d16fdbd90cfb` |
| `2023-dinov2.pdf` | 8,049,044 | 32 | `3add205547f3ece5fb1ac7a91720aa9fabf02d9cde29a096643ff022449f3e91` |

## Curation notes

- The filenames use the paper's commonly cited publication/preprint year, not the date this library was assembled.
- The collection intentionally keeps only the original YOLO paper. Later YOLO-family implementations can become a separate version-comparison study plan rather than obscuring the conceptual starting point here.
- Papers are stored for research and educational implementation. Preserve their original licenses and attribution; do not redistribute them as a new publication bundle without reviewing each source's terms.
