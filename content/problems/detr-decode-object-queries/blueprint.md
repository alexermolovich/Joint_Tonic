---
{
  "schema_version": 1,
  "problem_id": "detr-decode-object-queries",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Decode Normalized Boxes and Classes from Object Queries",
  "type": "function",
  "difficulty": "medium",
  "paper_ids": [
    "2020-detr"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2020-detr"
  ],
  "prerequisite_problem_ids": [],
  "entrypoint": "solution.decode_queries",
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
      "Normalized image frame: x right, y down"
    ],
    "units": {
      "boxes": "normalized image extent",
      "logits_scores": "dimensionless"
    },
    "axes": "B batch, Q query, C foreground classes; last class is no-object; boxes cxcywh to xyxy",
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
    "evaluator_sha256": "f3e61f68bf02843840a6c5785cc0acd1542f39bc456dd5cac148f7ad5a2609b6"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2005.12872"
    ],
    "implementation_urls": []
  }
}
---

# Decode Normalized Boxes and Classes from Object Queries

A DETR query is a prediction slot, not a guaranteed object. Its background score must compete with foreground classes. Decode the strongest foreground class first, then apply the supplied confidence threshold and padding mask; this exercise does not run matching or duplicate suppression.

```python
def decode_queries(logits, boxes, padding, threshold):
    ...
```

## Function contract

Inputs: `logits: float64(B, Q, C+1)`, `boxes: float64(B, Q, 4)`, `padding: bool(B, Q)` and a Python real `threshold` in `[0, 1]`. Bounds: `1<=B<=16`, `1<=Q<=128`, `1<=C<=64`.

The final logit represents no object. Include it in the stable softmax denominator, then select the greatest foreground probability, choosing the smallest class ID on ties. Boxes contain normalized `(center_x, center_y, width, height)`, with every entry in `[0, 1]`. Convert them to `(x1, y1, x2, y2)` and clip each endpoint to `[0, 1]`. Zero-sized boxes are allowed.

Return a dictionary with `boxes: float64(B, Q, 4)`, `scores: float64(B, Q)`, `labels: int64(B, Q)` and `valid: bool(B, Q)`. A slot is valid exactly when it is not padded and its foreground score is at least the threshold. Invalid slots have zero box/score and label `-1`. Query slots are independent; do not run NMS or assignment. Image coordinates point right/down and use the same normalized image extent per query.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** One query has logits `[0, 0]` (foreground, background), box `[.5,.5, 1, 1]`, no padding and threshold `.5`. Output: box `[0, 0, 1, 1]`, score `.5`, label `0`, valid `True`.

**Example 2.** Use the same input with threshold `.6`. Output: box `[0, 0, 0, 0]`, score `0`, label `-1`, valid `False`.

## Source and scope

Original bounded component based on [2020-detr](https://arxiv.org/abs/2005.12872). A grasping pipeline needs to distinguish a candidate from an empty query. Dropping the background logit makes uncertain predictions look certain. A decoded 2D box alone supplies neither object depth nor a collision-free grasp.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
