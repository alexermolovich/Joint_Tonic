# A score for shared image area

## Intuition

Raw intersection area favors large boxes. Dividing by the area covered by either box makes overlap comparable across sizes. A perfect match is 1; disjoint boxes are 0.

## The geometry

For continuous rectangles $A$ and $B$, define their intersection's lower corner by the coordinate-wise maximum of lower corners and upper corner by the minimum of upper corners. Negative extents mean separation, so clamp them to zero:

$$
w_{\cap}=\max(0,\min(x^A_2,x^B_2)-\max(x^A_1,x^B_1)),
$$

with the same expression for $h_{\cap}$. Then

$$
I=w_{\cap}h_{\cap},\quad U=|A|+|B|-I,\quad
\operatorname{IoU}(A,B)=\begin{cases}I/U,&U>0,\\0,&U=0.\end{cases}
$$

Coordinates are pixels, areas are square pixels, and the ratio is dimensionless. This task uses continuous rectangles; adding 1 to either extent changes the geometry.

## Broadcasting two sets

The axes mean different things. `boxes_a[:,None,:2]` has shape `(N,1,2)`, and `boxes_b[None,:,:2]` has shape `(1,M,2)`. Their maximum broadcasts to `(N,M,2)`, giving the lower intersection corner for every pair. Areas of A become `(N,1)`; areas of B become `(1,M)`. Keep those axes until the final `(N,M)` result.

## Visual walkthrough

Drag one box in the overlap view. The shared region is shaded once; the union is the total colored area. The score matrix highlights the row and column for the selected boxes. A table lists both areas, intersection, union, and ratio for the same pair.

## Worked numbers

Let A be `[0,0,4,2]` and B be `[2,0,6,2]`. Each area is 8, the intersection has width 2 and height 2, so $I=4$, $U=8+8-4=12$, and IoU is $1/3$. Translating both boxes by `(100,-5)` leaves all extents and the score unchanged.

## Why this matters on a robot

IoU appears in matching predictions to labels, choosing a responsible predictor, tracking, and duplicate suppression. A hidden change from continuous coordinates to pixel-inclusive coordinates alters evaluation and may change which obstacle detections survive postprocessing. Export the coordinate convention with the model's preprocessing and evaluator.

## Common failures

- Clamping a negative intersection area after multiplying two negative extents creates a false positive. Clamp each extent first.
- Returning a length-N vector assumes paired inputs rather than all N-by-M pairs.
- Dividing zero by zero creates NaNs for empty boxes.
- Swapping lower and upper corners silently can hide corrupt detection outputs; this contract rejects reversed boxes.

## Paper connection

[YOLO v1](https://arxiv.org/abs/1506.02640) uses overlap to connect predicted boxes and object confidence. IoU is a shared geometric primitive; this exercise focuses on that primitive and its edge cases rather than reproducing the detector.
