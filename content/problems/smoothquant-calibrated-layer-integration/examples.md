# Worked examples

calibration=[[2]], evaluation=[[4]], weights=[[2]], alphas=[0.5], tolerance=1e-9 gives scales=[[1]], selected_output approximately[[8]], output_mse approximately[0], row_max_abs approximately[[0]], accepted=[True], selected_index0, passed=True.

calibration=[[0,0]], evaluation=[[0,0]], weights=[[0],[0]], alphas=[0,1], tolerance=0 gives scales=[[1e6,1e6],[1e-6,1e-6]], outputs zero, output_mse=[0,0], row_max_abs=[[0],[0]], accepted=[True,True], selected_index0 and passed=True. The two guards/clamps differ while both exact-zero predictions agree.

