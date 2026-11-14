---
{
  "schema_version": 1,
  "problem_id": "sam-point-prompt-encoding",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Encode Positive and Negative Point Prompts",
  "summary": "Encode supplied positive/negative point coordinates with random Fourier features and learned-type vectors.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "segment-anything",
    "sam-point-prompt-encoding"
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
  "prerequisite_problem_ids": [],
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
  "entrypoint": "solution.encode_points",
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
    "evaluator_sha256": "289535773b7560b235f50657ae4932209c1d2ffa074471a5307a83b117a07b75"
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

# Encode Positive and Negative Point Prompts

Implement `encode_points(points: np.ndarray, labels: np.ndarray, image_size: tuple[int,int], frequencies: np.ndarray, type_embeddings: np.ndarray) -> np.ndarray`.

Encode supplied positive/negative point coordinates with random Fourier features and learned-type vectors.
points is float64 (N,2) with (x,y) pixel-index coordinates,0<=N<=4096; labels int64 (N,) is 0 negative or 1 positive. image_size is Python tuple (height,width), built-in positive ints<=100000. Require 0<=x<=width-1,0<=y<=height-1. frequencies is float64 (2,F),1<=F<=128,absolute values<=100; type_embeddings float64 (2,2F),row0 negative,row1 positive. Add 0.5 to each coordinate, divide by [width,height], map to [-1,1], multiply by frequencies and 2π. Return float64 (N,2F), concatenating ALL sine channels then ALL cosine channels, plus the corresponding type embedding. Frequencies and learned embeddings are supplied; do not sample random values. No padding label, resize, image encoder, or mask decoder is included.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. For image (1,1), point `[0,0]`, F=1, frequencies=`[[1],[0]]`, negative embedding `[0,0]` and positive embedding `[2,3]`: negative encodes `[0,1]`, positive `[2,4]`.
2. For image (2,2), point `[0,0]`, frequencies=`[[0.5],[0]]` and zero type vectors, normalized x=-0.5 and phase=-π/2; output `[-1,0]` (up to roundoff).

## Source and scope

[Primary source](https://arxiv.org/abs/2304.02643). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Form centered normalized coordinates, project frequencies and concatenate sine/cosine channels, then add type embeddings. O(NF) time/storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.

Source verification: [official prompt-encoder implementation](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/modeling/prompt_encoder.py) confirms the half-pixel offset, normalized random Fourier position features, and distinct point/corner embeddings. The exercise code and fixtures are original.
