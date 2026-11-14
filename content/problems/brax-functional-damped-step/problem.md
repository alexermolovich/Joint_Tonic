# Implement a Functional Physics Step Contract

## Goal

A functional step receives every state variable explicitly and returns a new state.

## Contract

functional_damped_step(position, velocity, force, mass, damping, dt) -> dict{position,velocity}. position/velocity/force float(B,D),0<=B<=4096,1<=D<=64,B*D<=100000; abs<=1e4. mass float(D,) values[1e-3,1e3] kg, damping float(D,) values[0,1e3] kg/s, dt scalar[1e-6,0.1] s. Positions m, velocities m/s, force N along independently modeled Cartesian axes in a common fixed frame. Float64 semi-implicit Euler: acceleration=(force-damping*velocity)/mass; next_velocity=velocity+dt*acceleration; next_position=position+dt*next_velocity. Explicitly no contacts, rotations, constraints, gravity unless supplied in force, or Brax/JAX backend reproduction. Return fresh arrays; validate all parameters even for empty batch. Bounded simple dynamics illustrates explicit immutable state, not stable integration for arbitrary parameters.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

position=[[0]],velocity=[[1]],force=[[3]],mass=[2],damping=[1],dt=0.1 -> velocity[[1.1]],position[[0.11]].

### Example 2

position=[[2]],velocity=[[0]],force=[[0]],mass=[1],damping=[0],dt=0.1 -> unchanged position[[2]],velocity[[0]].

## Source and scope

Original bounded component associated with [2021-brax](https://arxiv.org/abs/2106.13281). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
