# Independent review

Status: pending. Author checked the paired paper card and primary sources. Review mechanism scope, units/shape/masks, numerical examples, validation and grading before publication.


## Independent contract review — VLA research curator

Approved for implementation. Independently recomputed both worked examples and checked finite bounds, empty dimensions where supported, axes, units, masks, ownership and source scope. PointNet penalty sums matrix coordinates and averages only the batch; NeRF stratification uses an explicit equal-bin teaching convention; rendered depth is conditional foreground depth rather than an unnormalized moment. DINO normalized kNN voting preserves weighted ranking; DETR distinguishes padded target slots from no-object query labels; BEV is honestly described as a simplified global reduction.

Implementation attention: BEV allows positive subnormal weights. Normalize or rescale weights before multiplying features so a positive denominator cannot pair with an underflowed numerator. Add a subnormal-weight case. No source-specific full-model or robot-safety claim is made. Contract approval does not replace reference/evaluator checks.
