# Assign Ground-Truth Objects to Responsible Cells

## Intuition

The object center assigns responsibility to a grid cell. A cell cannot preserve multiple independent class targets in this bounded format, so collisions need an explicit and reproducible policy.

## Math and coordinate trace

For normalized image box $(c_x,c_y,w,h)$ and grid side $S$,
$$r=\lfloor Sc_y\rfloor,\quad c=\lfloor Sc_x\rfloor,\quad t=(Sc_x-c,Sc_y-r,w,h).$$
All values are dimensionless image fractions except integer row/column indices. The center offsets in $t$ are relative to the selected cell; sizes remain relative to the entire image. Among colliding objects choose largest area $wh$, then smallest input index.

| Quantity | Example | Meaning |
|---|---|---|
| Center | (0.75,0.25) | image fractions |
| Scaled center for S=2 | (1.5,0.5) | grid coordinates |
| Cell | row0,col1 | floor, with y as row |
| Local center | (0.5,0.5) | offset inside cell |

The image's upper boundary is excluded for centers so every center maps to a valid cell. Boxes may extend beyond the image because center ownership and corner clipping are separate decisions.

## Why this matters on a robot

Small adjacent objects may collide in a coarse grid even when their boxes are different. The explicit retained-object index makes lost supervision visible. This task assigns objects to cells; selecting a box predictor by IoU is a later training substep, not the same responsibility decision.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1506.02640). [decode-yolo-grid](/problems/decode-yolo-grid)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
