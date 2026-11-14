---
{
  "schema_version": 1,
  "problem_id": "sam-stability-overlap-filter",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Filter Automatic Masks by Stability and Overlap",
  "summary": "Filter Automatic Masks by Stability and Overlap",
  "type": "function",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "segment-anything",
    "paper-component"
  ],
  "paper_ids": [
    "2023-segment-anything"
  ],
  "paper_sections": [
    "Mechanism and explicit teaching conventions in theory.md"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "sam-mask-ranking"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.filter_stable_masks",
  "physical_contract": {
    "frames": [
      "Explicit caller grid/view frames in statement"
    ],
    "units": {
      "features": "dimensionless; BEV geometry in metres where stated"
    },
    "axes": "logits(N,H,W), quality(N); output original candidate indices(K).",
    "timestamp_assumptions": "One explicitly paired batch; no internal clock.",
    "batching": "logits(N,H,W), quality(N); output original candidate indices(K)."
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "validation",
      "edge-policy",
      "layout",
      "preservation",
      "independent-oracle",
      "scale"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching task; variants explicitly distinguished from full paper systems.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.02643"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/vision-vlm-3d/2023-segment-anything.md",
    "manifest": "research/manifests/vision-vlm-3d.md"
  },
  "owners": [
    "perception_implementation"
  ],
  "reviewers": ["vla_implementation"]
}
---

# Filter Automatic Masks by Stability and Overlap

## Contract

Implement filter_stable_masks(logits, quality, threshold, offset, stability_threshold, overlap_threshold).

logits is a finite NumPy float64 array (N,H,W), 0<=N<=128, 1<=H,W<=512, at most 1,000,000 entries, with absolute values <=1e6. quality is finite float64 (N,) with absolute values <=1e6; it is a ranking score and need not lie in [0,1]. Arrays may be noncontiguous.

The four scalar parameters are built-in int/float excluding bool. threshold is in [-1000,1000], offset in (0,1000], and stability_threshold and overlap_threshold in [0,1]. All are finite.

For candidate i, form three masks with strict > comparisons: base = logits[i]>threshold, high = logits[i]>threshold+offset, and low = logits[i]>threshold-offset. Stability is count(high)/count(low), or 0 when low is empty. Retain candidates only if the base mask is nonempty and stability>=stability_threshold.

Process eligible candidates in descending quality, breaking equal quality by smaller original candidate index. Greedily keep a candidate unless its binary base-mask intersection-over-union with ANY already kept mask is strictly greater than overlap_threshold. At equality it is kept. Return a new one-dimensional NumPy int64 array of original indices in processing order. Empty input or no eligible masks returns shape (0,).

All candidate masks refer to the same preprocessed image pixel grid; mask areas count pixels, and all scores are dimensionless. Preserve inputs. Non-array logits/quality raises TypeError; all other contract violations raise ValueError. No prompting, quality-head model, coordinate resizing, GPU, or gradient API is included.

This teaching variant suppresses by binary-mask IoU. The original SAM automatic generator uses box-based NMS stages; this exercise does not claim identical automatic-mask-generator output.

## Implementation and proof

Independent contract review precedes implementation. Test the examples, typed validation, boundary policies, input preservation and realistic scale with independent oracles. Publish only after isolated Run/Submit and starter-negative checks. Review risk: Check strict logit and IoU inequalities separately from inclusive stability; tie order, empty masks, mask-versus-box NMS distinction, and a suppressed candidate never suppressing later candidates.

## Resources and provenance

https://arxiv.org/abs/2304.02643. Actual shared local worker caps: 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. OCI image digest is pending; no image or reproducibility claim is invented. Original examples and future fixtures use CC0-1.0.

