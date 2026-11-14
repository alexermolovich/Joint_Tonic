# Worked examples

1. Scale 1, gravity [0,0,-9.81], zero biases, residual [0.2], valid [True], Jacobian [[1]], and limits [0.5,2,0.1,0.1,0.1,0.2,1e-6] pass all six checks. Rank is 1 and RMS is 0.2.
2. Jacobian rows [[1,0],[1,0]] have rank 1 despite two observations and zero residuals. The observability check fails, so the candidate is rejected even with a perfect residual fit.
