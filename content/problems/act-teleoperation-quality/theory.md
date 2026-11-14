# Detect Teleoperation Demonstration Quality Failures

## Intuition

A demonstration can look smooth in video while its logged joint stream contains impossible jumps or missing observations. Separate these failure types so a curator can inspect the evidence rather than discarding an entire dataset blindly.

## Mathematical mechanism

For joint j and row t>0, estimate 

$$v_{tj}=|q_{tj}-q_{t-1,j}|/(s_t-s_{t-1})$$

 in rad/s. Flag speed when any $v_{tj}>v^{max}_j$; range when any $q_{tj}<l_j$ or $q_{tj}>u_j$. Here q is the T by D joint array, s the T-vector of seconds, and l,u the D-vectors of bounds. Strict inequalities keep equality at a limit valid.

## Visual computation trace

| Row | Time | Joint | Observed | Flags with range[-1,1],speed1 |
|---|---|---|---|---|
| 0 | 0 | 0 | true | none |
| 1 | 1 | 2 | false | missing, range, speed |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

times=[0,1], joints=[[0],[2]], observed=[True,False], lower=[-1], upper=[1], max_speed=[1] returns missing=[False,True], out_of_range=[False,True], speed_jump=[False,True].

## Why this matters on a robot

Missing observations do not erase an actuator jump: masks are deliberately independent. Degrees mistaken for radians can trigger many false alarms, while an oversized speed threshold can hide an encoder fault. These flags support review, not automatic claims that the remaining trajectories are safe.

## Physical contract and limits

Joint positions radians; times seconds; max_speed radians/second, one threshold per joint. Time samples must be strictly increasing on one clock; differences are between adjacent recorded rows. Original demonstration-quality check motivated by ALOHA/ACT data collection. Thresholds are supplied; this is not a collision or contact-quality evaluator.

Source: [primary paper](https://arxiv.org/abs/2304.13705). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
