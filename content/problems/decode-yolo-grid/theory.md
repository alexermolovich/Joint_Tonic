# From local grid coordinates to a detector interface

## Intuition

Predicting a center relative to a nearby grid cell gives the model a local coordinate system. The decoder removes that local convention and returns ordinary image-space rectangles. This interface is small, but a mismatch here can make a well-trained detector appear completely broken.

## Mathematical map

Let the image width/height be $W,H$, grid columns/rows be $S_x,S_y$, and the current cell index be $(r,c)$. The prediction provides offsets $(t_x,t_y)$, direct image-relative size $(w,h)$, objectness $o$, and class values $p_k$.

$$
x_c=\frac{c+t_x}{S_x}W,\qquad y_c=\frac{r+t_y}{S_y}H,
\qquad w_p=wW,\quad h_p=hH.
$$

The rectangle is

$$
(x_1,y_1,x_2,y_2)=
(x_c-w_p/2,\ y_c-h_p/2,\ x_c+w_p/2,\ y_c+h_p/2).
$$

Clip these coordinates to the image's continuous extent. For class k, the output confidence is

$$
s_k=o\,p_k.
$$

The score cutoff is inclusive in this task. NMS will later choose between redundant boxes; decoding preserves the candidate set.

## Tensor map

The tensor axes are `(rows,columns,boxes,channels)`. Each box has its own C class values. This is an intentionally explicit teaching layout; the original YOLO v1 paper has a different full output layout and its training objective handles size differently. Later YOLO variants use additional codecs. A decoder must follow its declared interface rather than guess from the family name.

## Visual walkthrough

Select one cell in the grid view. It highlights `(r,c)`, draws the local offset to the predicted center, expands the width/height, clips at image edges, and shows each `objectness × class` score. A table lists those same intermediate quantities for keyboard and screen-reader access.

## Worked rectangular example

Take a 200x100 image, a grid of 2 rows and 4 columns, and cell `(r,c)=(1,2)`. Offsets `.25,.5` give center `(112.5,75)`. Direct sizes `.2,.4` give `(40,40)` pixels, so the box is `[92.5,55,132.5,95]`. With objectness `.8` and class probability `.5`, the score is `.4`.

## Why this matters on a robot

Image dimensions often change between a training crop, camera stream, and edge runtime. A decoder that scales x by height or uses stale resize metadata shifts target boxes. Store image preprocessing, grid layout, class order, codec version, threshold, and clipping behavior in one release artifact. Compare intermediate tensor outputs when moving inference between frameworks.

## Common failures

- Scaling width by the cell width instead of the full image width shrinks every box.
- Filtering class probability rather than the score product retains low-objectness noise.
- Converting the per-box class vector into only an argmax discards required candidates.
- An unstable sort makes equal-confidence outputs change across runtimes.
- Applying square-root or log decoding because another YOLO version does so violates this contract.

## Source and boundaries

[YOLO v1: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640), Section 2, motivates grid-relative unified detection. This exercise's codec, examples, and explanation are original and intentionally scoped to decoding; it does not reproduce the training loss or published model.
