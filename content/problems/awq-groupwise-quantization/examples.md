# Worked examples

weights=[[-1,1,0,3]], group_size=2,bits=2 gives scales=[[2/3,1]], zero_points=[[2,0]], quantized=[[0,3,0,3]], reconstructed=[[-4/3,2/3,0,3]]. Halfway rounding of -1/(2/3)=-1.5 uses -2 before adding zero point.

weights=[[0,0]], group_size=2,bits=4 gives scales=[[1]], zero_points=[[0]], quantized=[[0,0]], reconstructed=[[0,0]].
