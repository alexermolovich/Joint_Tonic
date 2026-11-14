# Evaluate Localization and Phrase Grounding Separately

A box can be geometrically correct while naming the wrong object, or name the right phrase while pointing elsewhere. Report these failures separately before combining them. The exercise receives matched pairs; it does not infer detection assignments or dataset precision.

```python
def grounding_pair_metrics(predicted_boxes, target_boxes, predicted_phrases, target_phrases, valid, iou_threshold):
    ...
```

## Function contract

Predicted/target boxes are `float64(N, 4)`, normalized `(x1, y1, x2, y2)` in `[0, 1]`, with strictly positive widths and heights. Predicted/target phrase IDs are `int64(N,)` in `[0, 100000]`. `valid` is `bool(N,)`, `0<=N<=4096`, and Python real `iou_threshold` lies in `[0, 1]`. Each row is an already matched pair in the same image and one fixed phrase vocabulary.

Compute paired IoU. Box correctness is validity AND `IoU>=threshold`; phrase correctness is validity AND equal phrase IDs. Joint grounding correctness requires both. Invalid rows have IoU zero and all flags false. Divide each true count by the number of valid rows, returning zero rates when none are valid.

Return `iou: float64(N,)`, `box_correct`, `phrase_correct`, `grounded_correct` as bool arrays `(N,)`; `count` as Python int; and `localization_rate`, `phrase_rate`, `grounded_rate` as Python floats. This is a paired diagnostic, not assignment, detection precision/recall, mAP or confidence calibration.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** An identical predicted/target box with different phrase IDs and threshold `.5` has IoU `1`, localization rate `1`, phrase rate `0`, and joint grounding rate `0`.

**Example 2.** Disjoint predicted/target boxes with the same phrase ID and threshold `.5` have localization rate `0`, phrase rate `1`, and joint grounding rate `0`.

## Source and scope

Original bounded component based on [2023-grounding-dino](https://arxiv.org/abs/2303.05499). A manipulation failure may come from perception geometry or language interpretation. One combined score can hide which subsystem needs attention. Supplied pairs must already share the same image and vocabulary; index equality across incompatible vocabularies is meaningless.
