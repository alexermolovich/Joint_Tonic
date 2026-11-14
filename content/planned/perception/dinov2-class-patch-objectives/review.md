# Author and independent review

Status: reviewed for implementation. Reviewer: vla_implementation.

## Proof of success

Verify cross-view pair normalization, mixed float32/float64 rejection, teacher stop-gradient, selected-patch global mean versus per-image mean, and empty/all-false patch graph behavior.

## Author evidence

Read the paired paper card and curriculum title. Source concepts were checked against the primary paper or official repository. All bounded APIs, examples, diagrams and text are original; scope differences are explicit. The theory has defined LaTeX, a static table and failure analysis. Reference/evaluator code does not exist yet.


## Independent review

Approved for implementation. All six draft files reviewed; both worked examples and class-pair counts independently recomputed. Independently checked the selected-patch gradient [-0.5,0.5] in example 1, zero gradient for the unselected patch branch, and detached teacher targets. The [official DINOv2 training implementation](https://github.com/facebookresearch/dinov2/blob/main/dinov2/train/ssl_meta_arch.py) combines class and masked-patch supervision with additional training details. The draft explicitly defines its own global selected-patch mean and excludes Sinkhorn/centering, KoLeo and distributed weighting.

Keep validation of all teacher rows, including masked-out entries; preserve the differentiable zero when P=0 or the mask is all false. Tests must distinguish the global selected-token mean from a per-image mean and exclude same-index global teacher/student class pairs.

Reference/evaluator checks and actual isolated Run/Submit remain publication gates.
