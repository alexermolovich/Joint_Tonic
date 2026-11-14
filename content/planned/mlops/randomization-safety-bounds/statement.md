# Choose Randomization Bounds from Safety Constraints

Implement constrain_randomization_bounds(nominal, requested, allowed, margins) -> dict.

nominal is NumPy float64(D,), requested and allowed float64(D,2), margins float64(D,),1<=D<=64. All values finite with absolute value<=1e6; margins>=0. Both input intervals have low<=high. Within dimension j all values use one caller-declared physical unit; different dimensions may use different units. Requested intervals and allowed intervals are absolute parameter values, not offsets. Shrink the allowed interval to[allowed_low+margins,allowed_high-margins], then intersect with requested to obtain lo=max(requested_low,shrunk_low), hi=min(requested_high,shrunk_high).

Return feasible:bool(D,), bounds:float64(D,2), failed_dimensions:int64(F,). A dimension is feasible iff lo<=hi AND lo<=nominal[j]<=hi; endpoints inclusive and zero-width intersections allowed. Bounds contain[lo,hi] only when feasible, otherwise[NaN,NaN]. failed_dimensions is sorted ascending input indices. Preserve inputs and return independent storage; noncontiguous input valid. Invalid contracts raise ValueError.

The allowed box and margins are supplied external constraints. This only checks independent interval feasibility and nominal inclusion. It cannot prove joint dynamic safety, simulator stability, collision freedom or hardware readiness; an infeasible box is a result, not an input error.

## Worked examples

### Feasible mass range
nominal[2], requested[[0.5,3]], allowed[[1,4]], margins[0.2] returns feasible[True], bounds[[1.2,3]], failed_dimensions[].

### Margin consumes allowed delay range
nominal[0.05], requested[[0,0.1]], allowed[[0,0.1]], margins[0.06] returns feasible[False], bounds[[NaN,NaN]], failed_dimensions[0].

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
