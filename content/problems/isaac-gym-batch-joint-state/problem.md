# Batch Independent Simulator States

## Goal

Simulator state is often exposed as a flattened buffer.

## Contract

batch_joint_states(flat_state, dof_indices) -> ndarray. flat_state float(A,2),0<=A<=100000, column0 joint position radians and column1 angular velocity radians/second. dof_indices int64(B,J),0<=B<=4096,1<=J<=256,B*J<=A and <=100000. Every selected index must be unique across ALL environments, in[0,A). Return float64(B,J,2) in given row/column order, fresh copy, no assumption rows are contiguous actors. Unselected flat rows are permitted and still validated. Empty B accepted even if A=0. This is a simplified homogeneous revolute-joint buffer gather, not an Isaac Gym actor API or prismatic/rigid-body layout.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

flat_state=[[1,10],[2,20],[3,30],[4,40]], indices=[[2,0],[3,1]] -> [[[3,30],[1,10]],[[4,40],[2,20]]].

### Example 2

flat_state shape(0,2), indices shape(0,3) -> shape(0,3,2). Repeated selected index raises ValueError.

## Source and scope

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
