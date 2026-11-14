## Worked examples

1. `reference=[0,1,2], queries=[0.1,0.5,1.9], tolerance=0.2` → `[0,-1,2]`. The middle sample is too far from both neighbors.
2. `reference=[0,2], queries=[1,0,2], tolerance=1` → `[0,0,1]`. The exact midpoint uses the earlier reference.
