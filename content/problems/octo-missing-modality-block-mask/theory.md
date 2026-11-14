# Build Block Masks for Missing Sensors and Goals

## Intuition

Attention visibility is a directed permission rule. An observation may read a goal without granting the goal access to every observation, and an absent token must be disabled as both a query and a key.

## Mathematical mechanism

Let $R\in\{0,1\}^{G\times G}$ be directed group visibility, $g_i$ the token group and $P_{bi}$ presence. $$A_{bij}=P_{bi}\land P_{bj}\land R_{g_i,g_j}.$$ B indexes examples; i and j index queries and keys. A missing goal cannot become visible simply because the observation group normally reads goals.

## Visual computation trace

| Query group | Task key | Observation key |
|---|---|---|
| task | true | false |
| observation | true | true |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

IDs=[0,1], rules=[[True,False],[True,True]], present=[[True,True]] gives [[[True,False],[True,True]]].

## Why this matters on a robot

An incorrect interface silently changes which sensor or actuator a feature describes. Preserve masks and schema versions when transferring to another robot.

## Physical contract and limits

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.

Source: [primary paper](https://arxiv.org/abs/2405.12213). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
