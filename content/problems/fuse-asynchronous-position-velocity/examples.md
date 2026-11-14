## Worked examples

1. `x=[0,0], P=eye(2), start_time=0, events=[[0,0,2],[0,1,4]], variances=[1,1], spectral_density=0` → means `[[1,0],[1,2]]`, covariances `[diag([0.5,1]),diag([0.5,0.5])]`.
2. `x=[0,1], P=zeros((2,2)), start_time=0, events=[[2,0,2]], variances=[1], spectral_density=0` → means `[[2,1]]`, covariance all zeros.
