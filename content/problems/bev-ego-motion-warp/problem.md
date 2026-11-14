# Warp a Previous BEV with Ego Motion

Implement warp_previous_bev(previous, previous_from_current, resolution, origin).

previous is a finite NumPy float64 array (H,W,C), with 1<=H,W<=256, 1<=C<=64, at most 1,000,000 entries and absolute values <=1e6. Features are dimensionless. Arrays may be noncontiguous. previous_from_current is finite float64 (3,3), absolute entries <=1e6, with bottom row [0,0,1] within atol=1e-7, rtol=0; its top-left rotation R satisfies R.T@R=I and det(R)=1 with the same tolerance. Treat its top two rows as supplied; do not project a near-valid rotation onto SO(2).

resolution is a finite built-in non-bool int/float in [1e-3,1e3], in metres per cell. origin is finite float64 (2,) with absolute values <=1e6, in metres. The current and previous grids use this same numerical origin and resolution in their respective local frames. Column increases +x, row increases +y; x,y,z form a right-handed frame. No image-down or vehicle-forward meaning is inferred.

For output row r and column c, its current-frame cell center is x=origin[0]+(c+0.5)*resolution, y=origin[1]+(r+0.5)*resolution. Apply previous_from_current to [x,y,1] to get the point in the PREVIOUS frame; no projective divide is used. Convert its previous coordinates to fractional array indices u=(x_previous-origin[0])/resolution-0.5, v=(y_previous-origin[1])/resolution-0.5.

Bilinearly sample the previous feature grid at (u,v), treating each out-of-bounds integer neighbor as an all-zero feature vector. Do not clamp coordinates, wrap indices, renormalize surviving weights, or simply reject a sample whose center lies outside the grid. A sample halfway beyond the final cell can retain half that cell's value. Return a new float64 array (H,W,C), preserving all inputs.

Non-array previous, previous_from_current or origin raises TypeError; all other violations raise ValueError. No empty spatial/channel axes, output-grid-size option, GPU, gradients, temporal attention, moving-object compensation or simulator is included. The transform is an already supplied pairing of adjacent ego frames; there is no internal clock or transform estimation. This is an explicit planar alignment exercise motivated by BEVFormer, not its complete temporal-attention implementation.

## Example 1: inverse lookup shifts sampled columns

~~~python
previous = np.array([[[1.],[2.],[3.]], [[4.],[5.],[6.]]])
previous_from_current = np.array([[1.,0.,1.],[0.,1.,0.],[0.,0.,1.]])
warp_previous_bev(previous,previous_from_current,1.,np.zeros(2))
# array([[[2.],[3.],[0.]], [[5.],[6.],[0.]]])
~~~

Each current cell asks for a location one metre farther along previous-frame x. A forward-scatter implementation would shift in the opposite direction.

## Example 2: partial border weights remain partial

~~~python
previous_from_current = np.array([[1.,0.,0.5],[0.,1.,0.],[0.,0.,1.]])
warp_previous_bev(previous,previous_from_current,1.,np.zeros(2))
# array([[[1.5],[2.5],[1.5]], [[4.5],[5.5],[3.]]])
~~~

The final output column samples halfway between the final stored column and a zero neighbor. It is neither clamped to the last value nor discarded entirely.


## Hints

1. Construct current cell centers, then map them into the previous frame using the supplied direction.
2. Subtract the grid origin and half-cell offset when converting metric positions to fractional array indices.
3. Use floor and four bilinear weights. Check each neighbor before indexing; do not renormalize boundary weights.

