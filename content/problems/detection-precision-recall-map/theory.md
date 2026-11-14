# Evaluate Detection with IoU, Precision-Recall, and mAP

## Intuition

Detection evaluation rewards finding distinct objects in score order. Repeating one correct box must not create extra recall, and a box in another image cannot match even when its coordinates are identical.

## Math and precision-recall trace

Within one class, let $h_k\in\{0,1\}$ mark the kth sorted prediction as a true positive under the stated one-use target matching rule. With $G$ ground-truth objects,
$$P_k=\frac{\sum_{j\le k}h_j}{k},\qquad R_k=\frac{\sum_{j\le k}h_j}{G}.$$
Build an upper precision envelope $\bar P_k=\max_{j\ge k}P_j$ and integrate it over positive recall increments, with zero precision after the final achieved recall. This gives all-point interpolated AP. Scores, IoU, precision, recall and AP are dimensionless.

| Ranked result | Cumulative TP | Precision | Recall with G=2 |
|---|---|---|---|
| correct A | 1 | 1 | 0.5 |
| duplicate A | 1 | 0.5 | 0.5 |
| correct B | 2 | 2/3 | 1 |

The second row adds no recall. AP is $0.5\cdot1+0.5\cdot(2/3)=5/6$. Averaging the three precision values would answer a different question. mAP averages AP only over classes with ground-truth coverage; absent classes are explicitly NaN.

## Why this matters on a robot

Duplicate detections can trigger duplicate task proposals. Evaluation should expose them, not silently reuse the same target. This single-threshold teaching metric is not COCO AP and does not reproduce the paper's benchmark protocol. Keep IoU threshold, class coverage and image identity attached to every score.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1506.02640). [box-iou-broadcast](/problems/box-iou-broadcast) · [class-aware-nms](/problems/class-aware-nms)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
