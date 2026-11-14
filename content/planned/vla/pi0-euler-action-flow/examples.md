# Worked examples

## Constant velocity on a nonuniform grid

initial=[[[2]]], times=[0,0.25,1], and velocity(state,time)=array([[[4]]]), all arrays float64.

trace=[[[[2]]],[[[3]]],[[[6]]]] and final=[[[6]]]. The two increments are1 and3; using a fixed step size would be wrong.

## A state-dependent field

initial=[[[1]]], times=[0,0.5,1], velocity(state,time)=state.

Euler gives trace=[[[[1]]],[[[1.5]]],[[[2.25]]]] and final=[[[2.25]]]. Reusing only the initial velocity would incorrectly produce2. The continuous exact solution at1 is e; this exercise grades the stated discrete Euler rule, not the exact ODE solution.
