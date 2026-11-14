# Joint Tonic first ten problems

**Status:** Approved authoring and implementation target  
**Version:** 0.1.0  
**Goal:** Build a complete, representative vertical slice before expanding the 183-problem roadmap.

These ten problems are selected to exercise the product's full learning loop: catalog metadata, original Theory pages, LaTeX, purposeful visuals, browser editing, public/hidden tests, physical contracts, paper provenance, progress, and multiple grading modes. They are small practical components, not claims of full paper reproduction.

## Selection summary

| # | Slug | Name | Domain | Difficulty | Primary source |
|---:|---|---|---|---|---|
| 1 | `se3-transform-points` | Apply an SE(3) Transform to Batched Points | Geometry | Easy | Foundation |
| 2 | `project-camera-points` | Project Camera Points into Pixels | Geometry/calibration | Medium | Foundation |
| 3 | `box-iou-broadcast` | Compute Pairwise Bounding-Box IoU | Perception | Easy | YOLO foundation |
| 4 | `decode-yolo-grid` | Decode YOLO Grid Predictions | Detection | Medium | YOLO v1 |
| 5 | `class-aware-nms` | Run Class-Aware Non-Maximum Suppression | Detection | Medium | YOLO deployment pipeline |
| 6 | `clip-symmetric-loss` | Compute Symmetric CLIP Contrastive Loss | VLM | Medium | CLIP |
| 7 | `rt1-action-codec` | Quantize and Decode Robot Actions | VLA | Medium | RT-1 |
| 8 | `diffusion-action-noising` | Add Noise to an Action Sequence | Robot learning | Medium | Diffusion Policy |
| 9 | `validate-robot-episodes` | Validate a Multimodal Robot Episode Schema | Robotics MLOps | Hard | Data Validation for ML + Open X-Embodiment |
| 10 | `edge-inference-release-gate` | Gate an Edge Model with Accuracy and Latency | Deployment/MLOps | Hard | MLPerf Inference + ML Test Score |

## 1. Apply an SE(3) Transform to Batched Points

- **Learner contract:** Transform one point `(3,)` or a batch `(N, 3)` from `camera` to `world` using a right-handed homogeneous transform. Translation is in meters.
- **Core math:**

  $$
  \mathbf p_w = \mathbf R_{wc}\mathbf p_c + \mathbf t_{wc}.
  $$

- **Visual:** 3D axes for source/target frames, points, and translation arrow; table fallback lists coordinates before/after.
- **Public cases:** identity, pure translation, 90-degree rotation.
- **Hidden families:** mixed rotation/translation, large batch, dtype tolerance, shape validation, input immutability.
- **Runtime:** Python/NumPy, CPU, 2 seconds, 256 MB.
- **Why first:** Tests the complete problem pipeline with simple deterministic fixtures and a high-value physical contract.

## 2. Project Camera Points into Pixels

- **Learner contract:** Project batched camera-frame points through a pinhole intrinsic matrix; return pixels, depths, and a validity mask for positive depth and image bounds.
- **Core math:**

  $$
  u=f_x\frac{x}{z}+c_x,\qquad v=f_y\frac{y}{z}+c_y.
  $$

- **Visual:** Camera frustum plus linked 2D image plane; dragging a 3D point updates its pixel and validity state.
- **Public cases:** optical axis, off-axis point, behind-camera point.
- **Hidden families:** zero/near-zero depth, boundary pixels, vectorized large batch, invalid intrinsics.
- **Runtime:** Python/NumPy, CPU.
- **Prerequisite:** Problem 1.

## 3. Compute Pairwise Bounding-Box IoU

- **Learner contract:** Compute an `(N, M)` IoU matrix for `xyxy` boxes without loops over pairs; degenerate boxes have zero area.
- **Core math:**

  $$
  \operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}.
  $$

- **Visual:** Two draggable rectangles with intersection/union shading and a live pairwise matrix.
- **Public cases:** identical, disjoint, partial overlap.
- **Hidden families:** empty arrays, degenerate/reversed coordinates according to documented policy, broadcasting, numerical stability.
- **Runtime:** Python/NumPy, CPU.
- **Paper connection:** Shared prerequisite for YOLO decoding/NMS/evaluation; paper card `research/papers/vision-vlm-3d/2016-yolo-v1.md`.

## 4. Decode YOLO Grid Predictions

- **Learner contract:** Convert cell-relative center offsets, width/height parameters, objectness, and class scores into sorted image-space detections.
- **Core math:** Explain grid offsets and declared width/height encoding in original notation; do not imply all later YOLO versions use the same codec.
- **Visual:** Interactive grid; selecting a prediction highlights the responsible cell and reconstructs the box step by step.
- **Public cases:** single cell/box, two classes, thresholded empty result.
- **Hidden families:** rectangular images, multiple boxes per cell, stable ordering/ties, clipping policy, invalid shapes.
- **Runtime:** Python/NumPy, CPU.
- **Paper connection:** YOLO v1 paper/card. Explicitly label this a teaching codec based on the original formulation.
- **Prerequisites:** Problems 2 and 3.

## 5. Run Class-Aware Non-Maximum Suppression

- **Learner contract:** Sort detections deterministically, suppress high-IoU boxes only within the same class, and return retained original indices.
- **Core math:** Greedy score ordering plus the IoU threshold rule.
- **Visual:** Step animation showing the chosen box, suppressed boxes, and IoU row; reduced-motion mode uses discrete steps.
- **Public cases:** overlapping same class, overlapping different classes, empty input.
- **Hidden families:** ties, threshold equality, nested boxes, many classes, stable indices, performance on thousands of boxes.
- **Runtime:** Python/NumPy, CPU, documented complexity target.
- **Paper connection:** Practical detection post-processing and deployment contract; paired with YOLO track while noting that NMS is a pipeline component rather than YOLO v1's novel contribution.
- **Prerequisite:** Problem 3.

## 6. Compute Symmetric CLIP Contrastive Loss

- **Learner contract:** Normalize paired image/text embeddings, apply a positive temperature, construct similarity logits, and average image-to-text and text-to-image cross-entropy.
- **Core math:**

  $$
  \mathcal L=\tfrac12\left[\operatorname{CE}(\mathbf Z_I\mathbf Z_T^\top/\tau,\mathbf y)+\operatorname{CE}(\mathbf Z_T\mathbf Z_I^\top/\tau,\mathbf y)\right].
  $$

- **Visual:** Similarity heatmap with paired diagonal, temperature slider, and row/column softmax views.
- **Public cases:** aligned orthogonal pairs, swapped pair, manual small logits.
- **Hidden families:** normalization, temperature validation, unequal/invalid shapes, gradient finiteness, duplicate-like negatives.
- **Runtime:** Python/PyTorch, CPU.
- **Paper connection:** `research/papers/vision-vlm-3d/2021-clip.md`.

## 7. Quantize and Decode Robot Actions

- **Learner contract:** Fit or consume per-dimension action bounds, map continuous actions to discrete tokens, reserve special-token space, and decode bin centers with clipping.
- **Core math:**

  $$
  q(a)=\operatorname{clip}\!\left(\left\lfloor B\frac{a-a_{\min}}{a_{\max}-a_{\min}}\right\rfloor,0,B-1\right).
  $$

- **Visual:** Action histogram with bin boundaries; moving an action shows token and reconstruction error per dimension.
- **Public cases:** lower/upper bounds, center values, batched round trip.
- **Hidden families:** per-dimension bounds, saturation, constant/invalid ranges, reserved offsets, maximum quantization error.
- **Runtime:** Python/NumPy, CPU.
- **Paper connection:** RT-1 paper/card; theory compares uniform bins with later quantile codecs without mixing their claims.

## 8. Add Noise to an Action Sequence

- **Learner contract:** Sample a diffusion timestep and Gaussian noise, construct a noised action sequence under a supplied schedule, preserve conditioning/mask semantics, and return the training target.
- **Core math:**

  $$
  \mathbf x_t=\sqrt{\bar\alpha_t}\,\mathbf x_0+\sqrt{1-\bar\alpha_t}\,\boldsymbol\epsilon.
  $$

- **Visual:** Time-series actions evolving from smooth trajectories to noise as timestep changes; show masked padding separately.
- **Public cases:** endpoints of a small schedule, seeded manual sample, padded chunk.
- **Hidden families:** batched timesteps, broadcasting, deterministic generator, masks, dtype/device, invalid schedule.
- **Runtime:** Python/PyTorch, CPU.
- **Paper connection:** `research/papers/vla-embodied/2023-diffusion-policy.md`.

## 9. Validate a Multimodal Robot Episode Schema

- **Learner contract:** Given episode records and a schema, report deterministic, located anomalies for required modalities, shapes, dtypes, ranges, units, frames, monotonic timestamps, action dimensions, and NaN/Inf values.
- **Theory:** Schema validation, example-level versus aggregate anomalies, training-serving skew, safe schema evolution, and why shape-valid data can still be physically invalid.
- **Visual:** Episode timeline and modality lanes; anomalies appear at their timestamp and schema path. Table fallback lists severity, path, episode, time, expected, and observed.
- **Public cases:** valid episode, missing camera frame, non-monotonic timestamps, out-of-range joint.
- **Hidden families:** optional fields, empty episodes, frame/unit mismatch, sensor dropout rate, unknown categories, deterministic error ordering.
- **Runtime:** Python standard library + NumPy, CPU.
- **Paper connection:** Data Validation for ML and Open X-Embodiment cards; uses original robot-specific schema and synthetic fixtures.
- **MLOps artifact:** Versioned schema plus validation report suitable for a pipeline gate.

## 10. Gate an Edge Model with Accuracy and Latency

- **Learner contract:** Aggregate benchmark samples into quality, p50/p90/p99 latency, throughput, memory, and slice regressions; return a structured release decision with every failed rule.
- **Core math:** Empirical quantiles, throughput from valid measurement windows, relative/absolute metric deltas, and minimum sample rules.
- **Visual:** Accuracy-latency scatter/Pareto view, percentile plot, and green/red gate table with accessible labels.
- **Public cases:** passing release, p99 failure, quality failure, insufficient sample.
- **Hidden families:** warm-up exclusion, dropped/invalid runs, multiple hardware classes, slice regression, threshold equality, deterministic reason order.
- **Runtime:** Python/NumPy, CPU.
- **Paper connection:** MLPerf Inference and ML Test Score cards; a teaching release gate, not an official MLPerf result.
- **MLOps artifact:** Immutable decision record including model, data, evaluator, preprocessing, runtime image, and hardware-class versions.

## Common authoring requirements

Every one of the ten must include:

- A completed Markdown blueprint based on `research/templates/problem-blueprint.md` before implementation.
- Original Problem, Theory, Solution, Submissions, and Notes content.
- Theory ordered as intuition → physical/tensor contract → LaTeX math → visual → worked example → robot relevance/failures → sources/boundaries.
- At least two public examples, public tests, hidden tests, a pinned runtime, a reference solution, and deterministic seeds.
- An explicit distinction between learner failure and platform/evaluator failure.
- A safe visualization payload and text/table fallback.
- Paper/source links without copied paper prose, figures, tables, or code.

## Vertical-slice completion order

1. Problems 1 and 3 establish schema, editor, NumPy runner, exact/numerical tests, and simple visuals.
2. Problems 2, 4, and 5 complete the geometry/detection mini-track and richer visual adapters.
3. Problems 6–8 add PyTorch, gradients/device rules, VLM/VLA theory, and time-series visuals.
4. Problems 9–10 add multi-file/system-style contracts, structured artifacts, MLOps grading, and release-decision UX.

Do not expand implementation beyond these ten until all ten pass the MVP acceptance criteria in `SPEC.md`; continue expanding research cards and discovery backlogs independently.
