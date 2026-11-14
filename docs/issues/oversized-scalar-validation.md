# Oversized integer scalars escape the documented ValueError contract

Status: fixed with content versions 1.0.1 and locally merged in `f4c5b05` after exact-diff review and sandbox regression checks. This issue draft was not posted remotely.

The shared scalar validator in four published perception exercises calls `math.isfinite(value)` before checking the documented numeric bounds. Passing `10**1000` as a threshold/epsilon raises `OverflowError` while converting the Python integer to a float. The declared contract requires `ValueError` for an out-of-range scalar.

Affected entrypoints introduced in `d045b0e`:

- `decode_queries` in `detr-decode-object-queries` (`threshold`).
- `class_token_logits` in `vit-class-token-linear-head` (`epsilon`).
- `neighbor_spreading` in `dinov2-neighbor-feature-spreading` (`epsilon`).
- `grounding_pair_metrics` in `grounding-localization-phrase-metrics` (`iou_threshold`).

Other packages may contain the same unused helper; changing unused copies is outside this focused issue. The unpublished NeRF integration is being corrected before promotion.

## Fix and proof

Use an isolated `codex/` branch/worktree. Reject values outside the permitted bounds before float conversion, while preserving type restrictions and NaN/Inf rejection. Add positive/negative huge-integer regressions to each affected evaluator, refresh evaluator digests and solution excerpts, and publish patch content versions because these packages already shipped. Verify the four reference Run/Submit cases and new boundary regressions. Do not change any in-range numerical behavior.

Prepare a local PR description until an authenticated GitHub issue/PR interface is available. Main reviews the exact diff and focused checks before merging.
