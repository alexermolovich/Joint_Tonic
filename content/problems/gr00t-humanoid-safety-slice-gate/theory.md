# Gate a Humanoid Policy Release on Safety Slices

## Intuition

A release decision needs evidence for every required scenario, not just a good overall score. Require enough trials, no recorded safety incidents, adequate success and acceptable latency while retaining optional failures for inspection.

## Mathematical mechanism

For slice s with $n_s$ trials, $k_s$ successes, $c_s$ incidents and latency $t_s$, $$pass_s=(n_s\ge n_{min})\land(c_s=0)\land(k_s/n_s\ge r_{min})\land(t_s\le T_{max}),\quad release=\bigwedge_{s:required_s}pass_s.$$ Required coverage prevents a high global average from hiding a failed robot scenario. Raw success fractions have sampling uncertainty; this teaching gate does not model confidence intervals or certify hardware safety.

## Visual computation trace

| Slice | trials/success | incident | required | decision |
|---|---|---|---|---|
| nominal | 10/9 | 0 | yes | pass at0.9 |
| contact recovery | 10/10 | 1 | yes | block |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

trials=[10,10],successes=[9,10],incidents=[0,1],latency=[20,10],required=[True,True],min_trials10,min_success.9,max_latency20 returns slice_pass[True,False],failures=[[],["safety_incident"]],releaseFalse.

## Why this matters on a robot

Aggregating incompatible robot channels or source types can hide a failing embodiment. Keep provenance, masks and per-slice results visible throughout training and evaluation.

## Physical contract and limits

Latency milliseconds; counts are evaluation trials/incidents, success rates dimensionless. Required slices are explicitly chosen scenario/embodiment conditions. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

Source: [primary paper](https://arxiv.org/abs/2503.14734). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
