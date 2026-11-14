# Author and independent review

Status: reviewed for implementation. Reviewer: vla_implementation.

## Proof of success

Check strict logit and IoU inequalities separately from inclusive stability; tie order, empty masks, mask-versus-box NMS distinction, and a suppressed candidate never suppressing later candidates.

## Author evidence

Read the paired paper card and curriculum title. Source concepts were checked against the primary paper or official repository. All bounded APIs, examples, diagrams and text are original; scope differences are explicit. The theory has defined LaTeX, a static table and failure analysis. Reference/evaluator code does not exist yet.


## Independent review

Approved for implementation. All six draft files reviewed; both worked examples independently recomputed using pixel sets. The [official stability function](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/utils/amg.py) confirms nested high/low threshold masks. The [automatic generator](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/automatic_mask_generator.py) uses box NMS, so the mask-IoU variant and explicit empty-mask policy are correctly labeled teaching choices.

Corrected grading metadata to exact output equality with zero tolerances because the result is ordered integer indices. Keep strict logit and suppression comparisons separate from the inclusive stability cutoff. Test a suppression chain so a rejected candidate cannot suppress a later mask.

Reference/evaluator checks and actual isolated Run/Submit remain publication gates.
