# Broadcast Batched Sensor Features

## Intuition

A robot's camera features change every timestep, while its tool or embodiment description may stay fixed for the episode. Attach the correct episode context to each present sample without accidentally sharing another robot's metadata.

## Episode and time axes

Let X in R^(B×T×F) be normalized sensor features, C in R^(B×K) episode context, and M in {0,1}^(B×T) presence. K is the context width named C in the function contract. Construct

$$Y_{bt,:}=\begin{cases}[X_{bt,:},C_{b,:}],&M_{bt}=1,\\0,&M_{bt}=0.\end{cases}$$

The output is B×T×(F+K). Broadcasting repeats context over time only; it never mixes batch rows. All features are dimensionless, and the caller has already aligned sensor frames and sample times.

## Visual shape trace and worked example

| Input | Shape | Example |
|---|---|---|
| sensor | (1,2,1) | [[2],[3]] |
| context | (1,1) | [9] |
| present | (1,2) | [true,false] |
| output | (1,2,2) | [[2,9],[0,0]] |

This static shape trace is also the text alternative.

## Why this matters on a robot

Repeating context along the wrong axis can silently assign the wrong gripper configuration to a sample. Filling context into absent timesteps can make padding look like real evidence. Keep presence explicit even when genuine feature vectors are all zeros.

Prerequisite: know the supplied episode/sensor schema; this task teaches robotic data alignment rather than Python syntax.

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
