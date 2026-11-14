# Select High-Gradient Image Points

## Intuition

Strong intensity changes constrain direct image alignment, but selecting only a global maximum concentrates evidence in one region. A fixed tile grid gives a simple reproducible coverage policy.

## Mathematics and conventions

For an interior pixel $(x,y)$, define central differences

$$g_x=\tfrac12(I_{y,x+1}-I_{y,x-1}),\quad g_y=\tfrac12(I_{y+1,x}-I_{y-1,x}),\quad s_{yx}=\sqrt{g_x^2+g_y^2}.$$

I is dimensionless grayscale intensity and s has intensity-per-pixel units. For tile width t, a pixel belongs to tile $(\lfloor y/t\rfloor,\lfloor x/t\rfloor)$. Within that tile, maximize s subject to $s>\tau$, using the row-major index $yW+x$ as the tie breaker. Borders lack a symmetric two-sided stencil and are excluded.

## Visual computation trace

| Image row | Interior gradients | Selection in one tile |
| --- | --- | --- |
| `[0,.25,.5,.75,1]` | dx=.25, dy=0 | all interior scores .25 |
| Earliest interior row | x=1,2,3 tie | select (1,1) |

## Worked examples

1. A `5x5` image whose rows are `[0.,0.25,0.5,0.75,1.]`, tile size `5`, threshold `0.1` yields coordinates `[[1,1]]` and score `[0.25]`. Every interior pixel ties; choose the earliest row-major one.
2. A constant `3x3` image, tile size `1`, threshold `0` returns empty coordinates of shape `(0,2)` and empty scores. Zero gradient does not exceed the threshold.

## Why this matters on a robot

Texture concentrated on a moving object can still mislead odometry. Gradient coverage supplies candidate evidence; it does not establish geometric consistency or compensate exposure changes.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1607.02565). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
