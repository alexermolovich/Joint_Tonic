# Author and independent review

Status: reviewed for implementation. Reviewer: vla_implementation.

## Proof of success

Independently test transform direction, nonzero origin, cell-center convention, rotation and fractional translations, partial zero padding, negative index wraparound, and nonmutation.

## Author evidence

Read the paired paper card and curriculum title. Source concepts were checked against the primary paper or official repository. All bounded APIs, examples, diagrams and text are original; scope differences are explicit. The theory has defined LaTeX, a static table and failure analysis. Reference/evaluator code does not exist yet.


## Independent review

Approved for implementation. All six draft files reviewed; both translation examples independently computed with scalar interpolation. Current-to-previous transform direction, half-cell centers, row=y/column=x, common numerical origin/resolution and per-neighbor zero padding are coherent. The [official BEVFormer implementation](https://github.com/fundamentalvision/BEVFormer/blob/master/projects/mmdet3d_plugin/bevformer/modules/transformer.py) confirms ego-motion handling, while the draft honestly declares a separate planar bilinear teaching interface rather than the full attention module.

Numerical guidance accepted by author: computing transformed world coordinates and subtracting a large origin can lose precision. At origin=1e6 and resolution=1e-3, the naive identity lookup incurs about -3.45e-8 index error. Use an equivalent stable index-space affine map such as R@[c+0.5,r+0.5]+((R-I)@origin+t)/resolution-[0.5,0.5], and cover large-origin identity, fractional borders, rotations, nonzero origins and negative-index rejection. This retains the documented mathematical contract.

Reference/evaluator checks and actual isolated Run/Submit remain publication gates.
