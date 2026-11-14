# Validate a Generated Reward Program

## Intuition

A small arithmetic reward language makes each generated term inspectable. Walk its syntax tree explicitly so the supported computations and resource limits are part of the contract.

## Mathematical mechanism

For a feature dictionary X whose arrays share B rows, interpretation maps each allowed syntax subtree to a vector in real B-space. A numeric constant $c$ becomes $c$ times the all-ones vector; a feature name selects its supplied vector. Arithmetic is elementwise: $$E(u+v)=E(u)+E(v),\quad E(u-v)=E(u)-E(v),\quad E(uv)=E(u)\odot E(v).$$ Unary signs preserve or negate the child vector. Each leaf has depth 1, and each operator has depth $1+\max(\text{child depths})$. Reject unsupported syntax before evaluation and reject any intermediate magnitude above 1e6. This is a deliberately restricted original teaching grammar, not the paper's full reward code.

## Visual computation trace

| Syntax subtree | Feature values | Evaluated reward |
|---|---|---|
| progress | [3,4] | [3,4] |
| 2*effort | [1,.5] | [2,1] |
| progress-2*effort | same batch | [1,3] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

expression "progress - 2 * effort", features progress [3,4], effort [1,.5] -> reward [1,3], used_features ["effort","progress"], node_count 10.

## Why this matters on a robot

A finite and well-scaled reward can still encourage the wrong behavior. Select policies with independent task and safety evidence; missing trials are not successful trials.

## Physical contract and limits

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

Source: [primary paper](https://arxiv.org/abs/2406.01967). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
