---
{
  "schema_version": 1,
  "problem_id": "sam-transform-prompt-coordinates",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Transform Prompt Coordinates Through Image Preprocessing",
  "type": "function",
  "difficulty": "easy",
  "paper_ids": [
    "2023-segment-anything"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2023-segment-anything"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.resize_prompt_coordinates",
  "owners": [
    "root"
  ],
  "reviewers": [
    "research_curator"
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
  "physical_contract": {
    "frames": [
      "Top-left image origin: x right, y down"
    ],
    "units": {
      "points": "continuous pixel-edge coordinates",
      "shape": "pixel counts"
    },
    "axes": "N,2 points in x/y order; returned shape height/width",
    "timestamp_assumptions": "Fixed supplied batch; cameras/observations are aligned by caller. No clock inference, state history or real-time guarantee.",
    "batching": "Only explicitly declared dimensions; masks preserve original ordering."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-mechanism-oracle",
      "boundary-and-invalid-input",
      "maximum-advertised-dimensions",
      "input-preservation-and-output-aliasing"
    ],
    "performance_class": "none",
    "evaluator_sha256": "114233d5c3044598b0cecf88b574eedea68555e85d09d1e6f05125ecf0bd66d1"
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
  }
}
---

# Transform Prompt Coordinates Through Image Preprocessing

Image preprocessing changes the coordinate system of a click or box corner. Rounding the resized image dimensions means each axis has its own realized scale. Transform prompts using those actual dimensions, not only the ideal longest-side scale.

```python
def resize_prompt_coordinates(points, image_height, image_width, target_length):
    ...
```

## Function contract

Input `points` is `float64(N, 2)`, where `0<=N<=4096`, ordered `(x, y)` in continuous pixel-edge coordinates. Require `0<=x<=image_width` and `0<=y<=image_height`. Image height/width are built-in integers in `[1, 8192]`; `target_length` is a built-in integer in `[1, 2048]`.

Compute `scale = target_length/max(image_height, image_width)`. Round the new height and width separately using `floor(original_size*scale + 0.5)`. Reject a result with either dimension zero. Scale x by `new_width/image_width` and y by `new_height/image_height`.

Return `points: float64(N, 2)` and `resized_shape: int64(2,)`, with shape ordered `(new_height, new_width)`. Origin remains top-left: bottom/right padding adds no offset. The rounding convention is part of this contract, independently of image-interpolation library behavior.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** An image of height 2 and width 4, resized to longest side 8, maps points `[[0, 0],[4, 2]]` to `[[0, 0],[8, 4]]` and returns shape `[4, 8]`.

**Example 2.** An image of height 3 and width 5, target length 4, rounds to shape `[2, 4]`. Point `[2.5, 1.5]` maps to `[2, 1]` using separately rounded axis scales.

## Source and scope

Original bounded component based on [2023-segment-anything](https://arxiv.org/abs/2304.02643). A segmentation prompt can miss a small grasp target if it is scaled with the unrounded image height. Confusing `(x,y)` with `(height,width)` is another common integration failure. These coordinates still require calibration before robot-frame use.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
