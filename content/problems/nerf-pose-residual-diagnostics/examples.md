# Worked examples

1. One valid sample with pixel residual `[3,4]`, RGB residual `[1,0,0]` gives pixel_rmse=5 pixels and color_rmse=1/√3. Limits (5,0.6) do not flag it; equality passes.
2. A view with no valid samples reports metrics 0 and observed=False, flagged=False, even at zero limits. Missing evidence is not perfect rendering.
