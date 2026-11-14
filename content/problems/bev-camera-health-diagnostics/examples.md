# Worked examples

1. received=`[[True,False]]`, valid=`[[True,False]]`, residuals=`[[[3,4],[0,0]]]`, limits (0.25,4) report dropout 0.5, RMSE 5, both alerts True.
2. An entirely missing two-frame window has dropout 1, RMSE placeholder 0, observed=False, calibration_alert=False. It may trigger dropout_alert, but supplies no calibration evidence.
