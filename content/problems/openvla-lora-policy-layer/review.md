# Independent contract review

Status: reviewed for implementation. Reviewer: curriculum_continuation. Draft author: vla_implementation.

Read blueprint, statement, theory, hints and examples, the paired OpenVLA card, relevant manifest and primary OpenVLA manuscript. Recomputed both numerical examples independently. No blocking contract issues remain. Corrected inherited generic blueprint metadata: actual feature axes/units and applicable exact fields now match the task rather than referring to action token IDs.

Verified OpenVLA §5.3 uses LoRA and the linked LoRA primary paper describes a frozen base with trainable low-rank update. The draft explicitly isolates one bias-free layer and supplies alpha/r scaling. Independently computed example1 output[-3,-4] and x-gradient[11,-9]; example2 output[6,-4], zero down-projection gradient and each up-projection gradient7. The contract correctly detaches only base weights while preserving base-branch x gradients, caller requires_grad settings, and zero-valued adapter graph connections at alpha0 or zero adapter parameters. Hidden tests must distinguish freezing the weight from detaching the base output and test gradient connectivity, noncontiguous layouts, both dtypes, and bounded values.

Primary sources: https://arxiv.org/html/2406.09246v3#S5.SS3 and https://arxiv.org/abs/2106.09685

Reference code, public/hidden evaluator, independent implementation review, and actual isolated Run/Submit remain required before publication. This is contract approval only.

Independent implementation review: curriculum_continuation approved both after LoRA huge-integer validation fix. Actual isolated Run2/Submit5 passed; empty starter and mechanism mutant rejected.
