# Aggregate Evaluation by Activity Slice

## Contract

activity_confusion_report(dataset_ids,truth,prediction,observed,num_classes) -> dict{dataset_ids,confusion,support,recall,macro_recall}. dataset_ids int64(N,) nonnegative,truth/prediction int64(N,),observed bool(N,),0<=N<=100000,num_classes built-in int1..64. For observed rows both labels must in[0,C); unobserved label placeholders may be arbitrary int64 and are ignored. Include all sorted dataset IDs, even with no observed labels. Return confusion int64(M,C,C) with axes(dataset,true,predicted), support int64(M,C) row sums,recall float64(M,C)=diagonal/support with NaN missing true classes; macro_recall float64(M,) mean only over supported true classes or NaN. Require M*C*C<=1e6. Predictions on absent true classes still count as columns for measured rows. This is a bounded classification diagnostic, not official Ego4D/Ego-Exo4D metrics for every task or robot-action supervision.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

dataset[0,0,0],truth[0,0,1],prediction[0,1,0],observed allTrue,C2 -> confusion[[[1,1],[1,0]]],support[[2,1]],recall[[.5,0]],macro[.25].

### Example 2

dataset[2,2],truth[-1,1],prediction[99,1],observed[False,True],C3 -> support[[0,1,0]],recall[[NaN,1,NaN]],macro[1].

## Source and scope

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). It does not reproduce the full dataset loader, task suite or headline results.
