# Unproject a Depth Map into a Point Cloud

Implement **unproject_depth(depth, K)**.

Accept real integer/floating array-like depth (H,W); either dimension may be zero. Depth is optical-axis z in meters, not Euclidean distance along a viewing ray. Values <=0, NaN, or either infinity indicate missing depth rather than an input error. Finite depth magnitudes must be <=1e6.

K is finite real (3,3), equal within atol=1e-9 and rtol=0 to [[fx,0,cx],[0,fy,cy],[0,0,1]], with 1e-6<=fx,fy<=1e6 and abs(cx),abs(cy)<=1e6. Reject bool, string, object, and complex arrays. All malformed inputs raise ValueError.

Return new float64 points (H*W,3) and bool valid (H*W,) in C row-major order. Pixel centers use integer (u=column,v=row), with no half-pixel offset. Positive finite depths produce [(u-cx)*z/fx,(v-cy)*z/fy,z] in the camera optical frame. Missing depths produce three NaNs and false. Preserve inputs and independent output storage.

All pixels are one static exposure. No distortion, world transform, depth-hole filling or occlusion reasoning.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-9. Masks, shapes and errors are exact.
