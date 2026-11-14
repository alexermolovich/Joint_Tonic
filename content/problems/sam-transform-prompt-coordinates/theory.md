# Transform Prompt Coordinates Through Image Preprocessing

## Intuition

Image preprocessing changes the coordinate system of a click or box corner. Rounding the resized image dimensions means each axis has its own realized scale. Transform prompts using those actual dimensions, not only the ideal longest-side scale.

## Mathematics and physical meaning

Original image height $H$ and width $W$ are positive pixel counts; the desired longest side is $L$. With $s=L/\max(H,W)$, the explicit half-up size convention is
$$H'=\lfloor Hs+0.5\rfloor,\qquad W'=\lfloor Ws+0.5\rfloor.$$
Reject a zero rounded dimension. Each input point $(x,y)$ uses continuous pixel-edge coordinates, including image boundaries, and transforms as
$$x'=x\frac{W'}W,\qquad y'=y\frac{H'}H.$$
The point array is $(N,2)$ in $x,y$ order; the returned shape is $(H',W')$, deliberately height first. Origin is top-left and axes point right/down. Later bottom/right padding adds no coordinate offset. This is a geometry component, not image interpolation or a learned prompt encoder.

## Visual trace

| Quantity | Before | After |
|---|---:|---:|
| Height | 3 | 2 |
| Width | 5 | 4 |
| Center x | 2.5 | 2 |
| Center y | 1.5 | 1 |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** An image of height 2 and width 4, resized to longest side 8, maps points `[[0, 0],[4, 2]]` to `[[0, 0],[8, 4]]` and returns shape `[4, 8]`.

**Example 2.** An image of height 3 and width 5, target length 4, rounds to shape `[2, 4]`. Point `[2.5, 1.5]` maps to `[2, 1]` using separately rounded axis scales.

## Why this matters on a robot

A segmentation prompt can miss a small grasp target if it is scaled with the unrounded image height. Confusing `(x,y)` with `(height,width)` is another common integration failure. These coordinates still require calibration before robot-frame use.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2304.02643). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
