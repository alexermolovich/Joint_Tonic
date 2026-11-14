# Build a Grounded Robot Perception Pipeline

## Intuition

A phrase score is not yet a robot-space location. The pipeline must connect segmentation evidence to depth, camera calibration, a world map, and operational health. Supplied masks and phrase scores isolate this interface without claiming trained-model inference.

## From pixels to world evidence

For pixel column $u$, row $v$, depth $z>0$ in meters and camera intrinsics $f_x,f_y,c_x,c_y$ in pixels, form a camera point and transform it:

$$p_c=((u-c_x)z/f_x,(v-c_y)z/f_y,z)^\top,\qquad p_w=R_{wc}p_c+t_{wc}.$$

$R_{wc}\in\mathbb R^{3\times3}$ and $t_{wc}\in\mathbb R^3$ are the supplied world-from-camera rotation and translation. Average the valid masked points for each query. The integer grid index is $(c,r)=\lfloor(\bar p_{w,x}+2,\bar p_{w,y}+2)\rfloor$ because the origin is $(-2,-2)$ meters and cell size is one meter. This centroid rule is an original simplification, not dense semantic BEV reconstruction.

## Temporal state and gate

With previous count map $B_{t-1}$ and current count map $C_t$, both shape $4\times4$,

$$B_t=0.5B_{t-1}+0.5C_t,\qquad r_{invalid}=1-N_{valid}/N_{eligible}.$$

The no-eligible case is defined as rate one. The fixed blend assumes aligned world cells; moving maps require an additional warp. Latency p95 sorts all supplied query durations and takes rank $\lceil0.95N\rceil$, counting from one.

| Stage | Example 1 trace | Failure exposed |
| --- | --- | --- |
| Mask and depth | one pixel, z=1 m | Empty/zero-depth mask |
| Unprojection | (0,0,1) camera | Wrong focal length |
| World/grid | row 2, column 2 | Transform direction or bounds |
| Blend and gate | count 0.5, promote | Stale state or missing evidence |

## Why this matters on a robot

The same good segmentation can land in the wrong map cell under a bad extrinsic transform. Masked invalid depth must not become an apparent point at the camera origin. Compare failures at each stage before changing thresholds; the synthetic verdict is not a robot safety authorization.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/2303.05499). [grounding-phrase-box-decoding](/problems/grounding-phrase-box-decoding) · [grounded-segmentation-failure-trace](/problems/grounded-segmentation-failure-trace) · [bev-temporal-fusion](/problems/bev-temporal-fusion)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
