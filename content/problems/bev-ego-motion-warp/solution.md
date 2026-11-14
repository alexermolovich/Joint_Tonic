# Solution

Use inverse lookup from current cell centers into the previous grid. Algebraically compute fractional index coordinates as R@[c+.5,r+.5]+((R-I)@origin+t)/resolution-.5; this avoids subtracting two large metric origins for identity motion. For each of four integer neighbors, add its bilinear contribution only where that neighbor is inside the grid. Do not clamp, wrap or renormalize. Output storage is independent, and complexity is O(HWC).
