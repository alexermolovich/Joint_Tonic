# Assemble Observation and Task Token Groups

## Intuition

A policy sees several token groups, such as a language goal, a camera and a state sensor. Concatenation must retain each group boundary and its presence mask; otherwise a missing sensor is indistinguishable from a real zero-valued observation.

## Mathematical mechanism

Group g has $X_g\in\mathbb R^{B\times N_g\times E}$ and Boolean $P_g\in\{0,1\}^{B\times N_g}$. Define offsets $o_0=0$, $o_{g+1}=o_g+N_g$. $$Y_{b,o_g+j,:}=P_{g,bj}X_{g,bj,:}.$$ Concatenate presence along tokens and assign group ID g even at absent positions. This keeps storage positions separate from availability.

## Visual computation trace

| Group | Tokens | Presence | Stored values |
|---|---|---|---|
| task0 | [1] | true | [1] |
| observation1 | [2,3] | true,false | [2,0] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

groups=[[[[1]]],[[[2],[3]]]], present=[[[True]],[[True,False]]] gives tokens=[[[1],[2],[0]]], present=[[True,True,False]], group_ids=[0,1,1], offsets=[0,1,3].

## Why this matters on a robot

An incorrect interface silently changes which sensor or actuator a feature describes. Preserve masks and schema versions when transferring to another robot.

## Physical contract and limits

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.

Source: [primary paper](https://arxiv.org/abs/2405.12213). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
