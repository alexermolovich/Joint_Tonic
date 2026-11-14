---
{
  "schema_version": 1,
  "problem_id": "sam-box-prompt-encoding",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Encode a Box Prompt with Positional Features",
  "summary": "Encode top-left and bottom-right box corners as distinct prompt tokens.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "segment-anything",
    "sam-box-prompt-encoding"
  ],
  "paper_ids": [
    "2023-segment-anything"
  ],
  "paper_sections": [
    "Prompt encoder: sparse point and box positional/type embeddings"
  ],
  "track_ids": [
    "paper-2023-segment-anything"
  ],
  "prerequisite_problem_ids": [
    "sam-point-prompt-encoding"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.encode_boxes",
  "physical_contract": {
    "frames": [
      "Resized image pixel-index coordinates"
    ],
    "units": {
      "values": "pixels and dimensionless embeddings"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "a8428084c60ee5b67df4a15f8ebba53847badf15b5745eb3941ffc51faaae038"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.02643"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Encode a Box Prompt with Positional Features

Implement `encode_boxes(boxes: np.ndarray, image_size: tuple[int,int], frequencies: np.ndarray, corner_embeddings: np.ndarray) -> np.ndarray`.

Encode top-left and bottom-right box corners as distinct prompt tokens.
boxes is float64 (N,4) ordered (x1,y1,x2,y2),0<=N<=2048, with 0<=x1<=x2<=width-1 and 0<=y1<=y2<=height-1 in pixel-index coordinates. Degenerate equal corners are allowed. image_size tuple (height,width) uses positive built-in ints<=100000. frequencies float64 (2,F),1<=F<=128,absolute values<=100; corner_embeddings float64 (2,2F),row0 top-left,row1 bottom-right. For each corner add 0.5, divide by [width,height], map to [-1,1], form phase=2π*q@frequencies, concatenate sine then cosine channels and add that corner's vector. Return float64 (N,2,2F), preserving box and corner order. This encodes supplied boxes; it neither predicts boxes nor decodes masks.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. In image (1,1), box `[0,0,0,0]`, frequencies=`[[1],[0]]`, corner vectors `[[1,2],[3,4]]` gives `[[[1,3],[3,5]]]`.
2. In image (2,2), box `[0,0,1,1]`, frequencies=`[[0.5],[0]]`, zero corner vectors gives top-left `[-1,0]` and bottom-right `[1,0]`.

## Source and scope

[Primary source](https://arxiv.org/abs/2304.02643). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Vectorize the same Fourier map over box and corner axes, then add distinct corner vectors. O(NF) time/storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.

Source verification: [official prompt-encoder implementation](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/modeling/prompt_encoder.py) confirms the half-pixel offset, normalized random Fourier position features, and distinct point/corner embeddings. The exercise code and fixtures are original.
