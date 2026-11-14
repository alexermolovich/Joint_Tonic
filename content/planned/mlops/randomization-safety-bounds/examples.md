# Worked examples

### Feasible mass range
nominal[2], requested[[0.5,3]], allowed[[1,4]], margins[0.2] returns feasible[True], bounds[[1.2,3]], failed_dimensions[].

### Margin consumes allowed delay range
nominal[0.05], requested[[0,0.1]], allowed[[0,0.1]], margins[0.06] returns feasible[False], bounds[[NaN,NaN]], failed_dimensions[0].
