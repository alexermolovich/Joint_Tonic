# Check a Segment Against Occupancy Cells

## Intuition

Testing a few points along a path can miss an obstacle between samples. Intersect the continuous segment with each occupied cell so even a corner touch is handled by an explicit policy.

## Mathematics and physical meaning

Parameterize the segment as $p(t)=a+t(b-a)$ for $t\in[0,1]$. A closed cell bounds x and y independently. For coordinate $j$ with direction $d_j\ne0$, allowable t values are between $(l_j-a_j)/d_j$ and $(h_j-a_j)/d_j$, reordered if necessary. Intersect both coordinate intervals with $[0,1]$:
$$t_{\mathrm{enter}}=\max(0,t_{x,\min},t_{y,\min}),\quad t_{\mathrm{exit}}=\min(1,t_{x,\max},t_{y,\max}).$$
There is contact when $t_{\mathrm{enter}}\le t_{\mathrm{exit}}$. If $d_j=0$, the starting coordinate must lie within that slab for any intersection to be possible. This also handles a zero-length segment.

## Visual trace

| Segment relative to occupied [1,2]×[1,2] | Result |
|---|---|
| [0,1.5] -> [3,1.5] | blocked, passes through |
| [0,0] -> [1,1] | blocked, corner touch |
| [0,0] -> [3,0] | free |

This static table is also the text alternative; no animation is required.

## Worked examples

1. In a 3×3 zero grid with grid[1,1]=1, start=[0,1.5], end=[3,1.5] → False.
2. Same grid, start=[0,0], end=[3,0] → True. A segment ending at [1,1] instead returns False because the occupied corner is touched.

## Why this matters on a robot

A point path is safe for a finite-size robot only after obstacles are inflated by an appropriate footprint and margin. This exercise checks exact line/cell intersection under a point-robot contract; it does not provide that inflation or dynamic obstacle prediction.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
