# Worked examples

1. Map corners `[[-1.,-1.,0.],[-1.,1.,0.],[1.,-1.,0.],[1.,1.,0.]]`, query `[[0.,0.,1.]]`, K=4, radius 2, tolerance 0 yield centroid `[[0.,0.,0.]]`, normal `[[0.,0.,1.]]`, offset `[0.]`, valid `[True]`. Equal-distance neighbor indices follow `[0,1,2,3]`.
2. Map points on one straight line, such as `[[0.,0.,0.],[1.,0.,0.],[2.,0.,0.]]`, have zero second eigenvalue. The fit is invalid and normal/offset are NaN, even if every neighbor is within radius.
