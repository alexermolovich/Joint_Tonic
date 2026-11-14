# Check a Segment Against Occupancy Cells

Check a continuous point-robot segment against closed occupied grid cells, including grazing contact.

```python
def segment_is_free(grid, start, end):
```

## Contract

Grid contains integer-valued zeros and ones (real numeric dtype; boolean dtype follows the general rejection policy). Endpoints must lie in the closed map rectangle [0,W]x[0,H]. Occupied row r,column c is the closed square [c,c+1]x[r,r+1]. Return False if any point of the closed segment touches/intersects any occupied square; otherwise True. Boundary contact counts as collision. Equal endpoints are valid. Do not use sparse sampling that can skip a thin crossing.

**Shapes and outputs:** grid(H,W), 1<=H,W<=128, start/end(2,) -> Python bool.

**Units:** start,end: metres, grid: binary occupancy. **Time:** One static occupancy snapshot; obstacles do not move.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. In a 3×3 zero grid with grid[1,1]=1, start=[0,1.5], end=[3,1.5] → False.
2. Same grid, start=[0,0], end=[3,0] → True. A segment ending at [1,1] instead returns False because the occupied corner is touched.
