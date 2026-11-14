# Worked examples

1. Estimated tetrahedron points `[[0,0,0],[1,0,0],[0,1,0],[0,0,1]]` as float64, reference `2*Rz(90deg)*point+[1,2,3]`, fit_scale=True: recovered scale 2, rotation Rz(90deg), translation `[1,2,3]`, RMSE zero up to floating error.
2. Use the same reference but fit_scale=False: scale remains exactly 1. The best rigid alignment still has nonzero error because translation and rotation cannot absorb the factor-of-two scale difference.
