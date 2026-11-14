# Independent perception draft review

Reviewer: `paper_explanations`. Scope: source, mathematical explanation, API boundaries, worked examples, and evaluation plan. Approval here permits implementation; isolated evaluator verification remains separate.

## First pair

- **ViT / resolved:** a zero-image batch bypassed the total-element cap and left spatial dimensions effectively unbounded. The author added explicit bounds to B, C, H, W, and patch size, including `image_shape`; the reviewer reread the corrected contract. The index equation, rectangular example, channel order, and separate direct-token check correctly distinguish a valid layout from a merely invertible wrong permutation. Independent element-by-element calculation confirms both examples.
- **CLIP / approved:** row normalization, same-shape paired batches, explicit nonzero norm range, independent storage, and gradient contract are consistent. Independent numerical calculation confirms both examples and the Jacobian row `[0.128,-0.096]` at `[3,4]`. The bounded CPU API is correctly identified as an educational choice. Source: [CLIP §2.3](https://arxiv.org/abs/2103.00020).

## Remaining first-batch review

- **DETR / resolved:** the size range `(0,1]` admitted values too small to survive center-to-corner conversion in float64. For example a width/height of `1e-20` at center `0.5` yields equal floating-point corners and zero union/enclosure. The author added the teaching lower bound `1e-6` for width and height and synchronized the explanation and blueprint. Negative probability, center-size L1, and negative-GIoU semantics match the [official matcher](https://github.com/facebookresearch/detr/blob/main/models/matcher.py); the constant differs from `1-GIoU` intentionally. Independent arithmetic confirms both cost examples. Include below-bound rejection in implementation checks.
- **PointNet / approved:** channelwise masked maximum and joint feature/mask permutation are correctly distinguished from selecting one point or rotating the cloud. Negative-value padding, duplicate points, and empty valid sets have explicit behavior. Both examples and the reindexing proof were independently checked against the [PointNet mechanism](https://arxiv.org/abs/1612.00593).
- **NeRF / approved:** density and interval units cancel, transmittance is exclusive, and the finite final interval leaves explicit background mass. Both examples were independently recomputed with a sequential mass-conservation oracle. The no-infinite-tail teaching boundary is explicit and consistent with the selected [rendering equation](https://arxiv.org/abs/2003.08934).
- **DINOv2 / approved:** EMA uses post-step student parameters, pairs by name, and returns detached independent snapshots. Buffers and schedules are explicitly outside this API. Independent arithmetic confirms both examples and the second update `[2.16,4.04]`; the equation agrees with the [official teacher update](https://github.com/facebookresearch/dinov2/blob/main/dinov2/train/ssl_meta_arch.py). Empty dictionaries and zero-element tensors need behavior checks during implementation; do not use nonzero data pointers as the sole storage test for empty tensors.

## Executable peer review, first six

The new runtime packages include original reference implementations, public and hidden evaluators, starter code, solutions, and static theory trace tables. Independent reviewer `vla_implementation` checked the six implementations and grading coverage. Actual local bubblewrap Run and Submit passed 47 grading cases in total.

- **DETR / fixed:** peer review found that a built-in integer weight such as 10**1000 reached NumPy finiteness checking before its documented bounds check, producing TypeError instead of ValueError. Bounds now reject it first; a regression was added and isolated Run/Submit passed again.
- **DINOv2 / fixed during follow-up:** the analogous arbitrary-size integer momentum is rejected by its range check before conversion in math.isfinite. A regression is included.
- All six use the actual shared worker caps. Image digest remains pending for the local baseline; no training-reproduction claim is made. The rendered theory uses static shape/numerical tables, with matching text explanations, rather than relying on unsupported Mermaid rendering.

## Executable peer review, second and third batches

Independent reviewer `vla_implementation` approved the six packages numbered 107–112 after checking their reference implementations, boundary contracts, and grading behavior. The ViT token contract now explicitly bounds the named dimensions B, N, F, and D by 1024 while allowing the positional sequence length N+1 to reach 1025. All 39 grading cases passed isolated Run and Submit.

The same reviewer approved packages 113–118 after focused reference review. In particular, the BEV aggregator rescales positive weights before feature multiplication, preserving the documented positive-subnormal case; conditional NeRF depth uses the declared foreground-mass threshold; and weighted kNN evaluation handles empty queries and stable ties. All 35 grading cases passed isolated Run and Submit. All twelve new starters were rejected as expected by Submit. No blocking findings remain for these batches.

## Publication boundary

Use the actual enforced local worker runtime and caps in published packages: Python 3.12.3, NumPy 2.2.4, PyTorch 2.6.0+cpu where applicable, bwrap-v2; wall 18 seconds, CPU 10 seconds, 4 GiB address space, 64 KiB output. Draft tighter budgets are targets, not enforced per-problem settings. Require public and hidden reference checks through the isolated worker before catalog registration.

## Fourth batch, first three contract reviews

Reviewer vla_implementation independently checked DETR Hungarian assignment, ViT position interpolation and CLIP prompt ensembling. Six examples and the ViT class/spatial gradient were recomputed. All three are approved for implementation. The only correction was to the rectangular Hungarian dual explanation: query potentials must be nonpositive, with zero potential on unused queries at an optimum; the theory now states this. Detailed primary-source links and implementation edge guidance are recorded in each review.md.

## Fourth batch, remaining three contract reviews

Reviewer vla_implementation independently checked SAM stability/overlap filtering, DINO class/patch objectives and BEV ego-motion warping. Six examples, teacher stop-gradient and selected/empty patch gradients pass independent calculations. SAM grading metadata now requires exact ordered integer output. The author accepted stable BEV index-space sampling guidance after reproduction of large-origin cancellation, and will add that regression. All three contracts are approved; their documented SAM mask-NMS, DINO loss-reduction and BEV alignment scope differences are preserved.

## Fourth batch publication and code review

All six packages, numbered 119–124, are published after independent code/evaluator approval by `vla_implementation`. The actual unchanged bubblewrap worker passed 42 Submit cases and 18 public Run cases in staging; all six unfinished starters were rejected. Staging used the current worker harness with an author-process-only content-root override, so learner isolation and enforced resource caps were unchanged.

The evaluators include a brute-force small assignment oracle and planted large optimum, an independent cubic interpolation value/gradient oracle, scalar prompt-vector arithmetic, set-based mask overlap, independently derived DINO student gradients and teacher stop-gradient checks, and scalar BEV sampling plus large-origin identity regression. BEV uses the accepted algebraically equivalent index-space transform to avoid subtracting large metric origins. Paper-flow nodes and corresponding explanation sections now link each exact runnable component; the former planned titles were removed from those nodes.
