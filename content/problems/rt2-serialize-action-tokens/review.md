# Independent contract review

Status: reviewed. Reviewer: code_issue_scout.

Verified RT-2 primary section3.2 and paired card. Nonmonotone vocabulary examples independently map to [0,41,99] and [1,7,41], and [0,3]. Injective supplied mapping, reserved flag grammar and fixed field width are explicitly original. Empty batch, whole-batch rejection, dtype/range and storage contracts are clear. Integer grading metadata corrected to exact/0/0 before approval.

Read all six draft files, paired source cards and primary manuscript sections. Independently recomputed both worked examples. No blocking contract findings remain. Reference implementation, tests and actual isolated evaluator verification remain separate.

## Independent implementation review

Reviewer code_issue_scout approved the reference and evaluator after checking vocabulary/inverse mapping, whole-batch rejection, empty/noncontiguous arrays, exact integer equality, Euler left-endpoint state/time evaluation, callback exception identity, storage and permitted intermediate action states. Independently checked an additional RT2 round trip and Euler grid [0,0.125,0.5,1] with velocity 1+2t, yielding trace [1,1.125,1.59375,2.59375]. No blocking findings.

## Isolated runtime verification

Reference passed 6 unique public/hidden cases through actual bubblewrap Run and Submit. The unchanged worker sandbox and harness were pointed at an authoring-only temporary content root; the complete package was moved into the live catalog only after verification. The starter was rejected by Submit. Runtime: Python 3.12.3, NumPy 2.2.4, bwrap-v2; 18 seconds wall, 10 CPU seconds, 4096 MiB address space and 64 KiB output. Evaluator SHA-256 is pinned in blueprint.md; OCI image digest remains pending.
