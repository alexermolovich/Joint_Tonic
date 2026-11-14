# Integrate an Action Flow with Euler Steps

Implement euler_action_flow(initial, times, velocity), returning (final, trace). initial is a finite NumPy float64 array(B,H,D), abs values<=1e6, with1<=B<=16,1<=H<=64,1<=D<=32. times is finite float64 shape(K+1,),1<=K<=128, starts exactly0, ends exactly1 and is strictly increasing. Require (K+1)*B*H*D<=1,000,000. Each array may be noncontiguous.

velocity is callable. At step k call it exactly once as velocity(state, float(times[k])). It returns a finite float64 ndarray with the state's exact shape and absolute entries<=1e6, interpreted as velocity in normalized action coordinates per unit dimensionless flow time. Evaluator callbacks are deterministic, do not mutate arguments and may depend on both state and time. Do not call at the final time1.

Update state <- state + (times[k+1]-times[k])*velocity(state,times[k]). Record the initial state and every updated state in trace(K+1,B,H,D). final(B,H,D) equals trace[-1] numerically but is an independent copy; neither output aliases either input or the other output. Preserve inputs. Callback outputs may alias its input, so consume them without mutation. Callback-thrown exceptions propagate unchanged.

Raise TypeError for non-array initial/times or non-callable velocity. Raise ValueError for input-contract violations or callback return-contract violations, including a non-array callback result. There is no tensor autograd, random sampling, clipping, adaptive solver, observation encoder or hardware execution. Initial noise is supplied; every output has the same normalized Euclidean action-channel semantics, frame and horizon ordering as initial. Flow time is not robot-control time. Sum of positive step sizes is1, so declared input/velocity bounds keep accumulated states finite.

## Sources and scope

[Primary paper](https://arxiv.org/pdf/2410.24164v4), SectionIV and AppendixA-D: forward Euler inference. This is a bounded original component, not the paper's complete model.


## Worked examples

### Constant velocity on a nonuniform grid

initial=[[[2]]], times=[0,0.25,1], and velocity(state,time)=array([[[4]]]), all arrays float64.

trace=[[[[2]]],[[[3]]],[[[6]]]] and final=[[[6]]]. The two increments are1 and3; using a fixed step size would be wrong.

### A state-dependent field

initial=[[[1]]], times=[0,0.5,1], velocity(state,time)=state.

Euler gives trace=[[[[1]]],[[[1.5]]],[[[2.25]]]] and final=[[[2.25]]]. Reusing only the initial velocity would incorrectly produce2. The continuous exact solution at1 is e; this exercise grades the stated discrete Euler rule, not the exact ODE solution.


## Hints

1. Validate the complete contract before producing a result.
2. Follow the declared field or time ordering; preserve metadata rather than guessing.
3. Return fresh arrays and verify both worked examples before handling larger batches.


## Runtime and tolerances

Python 3.12.3; NumPy 2.2.4. Shared worker limits: 18 seconds wall time, 10 seconds CPU, 4096 MiB memory and 64 KiB output. Numerical comparisons use rtol=0.000001 and atol=1e-7 unless an exact boolean/integer result is specified. Synthetic fixtures are CC0-1.0.
