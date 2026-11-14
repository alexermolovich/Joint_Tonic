# Review and runtime verification

Status: reviewed and implemented. Prior draft author: vla_implementation. Contract reviewer: curriculum_continuation. Independent implementation reviewer: root.

The prior draft was checked against the paired RT-2 card and primary manuscript section 3.2, Output Constraint. The source constrains the action vocabulary; this problem explicitly uses an original fixed-width grammar and deterministic greedy choice rather than claiming the paper's tokenizer or full sampling loop. Both examples, tensor/ID contracts, numeric tie breaking, masked normalization, empty batches, and the distinction between syntax and robot safety were reviewed before implementation.

Root independently reviewed problem.md, reference.py and cases.py, approving allowed-only stable softmax, numeric-ID tie handling, independent scalar oracle, empty and scale checks. No blocking findings remain.

Eight unique public/hidden cases passed trusted reference checks and actual isolated bubblewrap Run (3 public) plus Submit (all 8). The starter failed Submit. Two intentional mutants were rejected: resolving ties by vocabulary order, and normalizing the full vocabulary before masking. The bounded scale case covers width65536 and a batch near1000000 entries. Tests assert exact forbidden zeros and exact token IDs, declared floating tolerances, preservation and nonaliasing, noncontiguous layouts, complete-batch validation, and empty shape behavior.

Verification used Python3.12.3, NumPy2.2.4, existing bwrap-v2 sandbox and its fixed18s wall/10s CPU/4096MiB address-space/64KiB output caps. No evaluator or dependency changed. The evaluator hash is recorded in metadata and blueprint; an OCI image digest remains pending, so this is the local runtime baseline.

Published package: [rt2-constrained-action-decoding](../../../problems/rt2-constrained-action-decoding/).
