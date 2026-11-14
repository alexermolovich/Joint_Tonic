# Evaluate Foot Clearance Across Terrain Slices

## Intuition

Foot height becomes useful only relative to the nearby support surface. Compare observed swing feet against that surface, then retain separate terrain slices so easy ground cannot hide clearance failures elsewhere.

## Mathematical mechanism

For environment $b$, synchronized time $t$ and foot $f$, let $p_{btf}\in\mathbb R^3$ be a world-frame foot position and $h_{btf}$ the supplied terrain height immediately below it, both in meters with world z up. Boolean swing and observed masks define $E_{btf}=S_{btf}\land O_{btf}$. Clearance is
$$c_{btf}=p_{btf,z}-h_{btf}.$$
Write NaN outside $E$; keep negative eligible clearances. Each environment has one terrain identifier $g_b\in\{0,\ldots,K-1\}$. For terrain $k$, define $I_k=\{(b,t,f):E_{btf}\land g_b=k\}$ and $n_k=|I_k|$. Given minimum clearance $\tau_k$ in meters,
$$\mu_k=\frac{1}{n_k}\sum_{i\in I_k}c_i,\qquad m_k=\min_{i\in I_k}c_i,\qquad v_k=\frac{1}{n_k}\sum_{i\in I_k}[c_i<\tau_k].$$
Return NaN for all three statistics when $n_k=0$. Equality passes the threshold. Every observed swing foot/time sample has equal weight; this is neither an episode-balanced nor a time-duration-weighted average. The supplied height is already associated with each foot; interpolation and contact estimation are outside this component.

## Visual computation trace

| Foot sample at threshold .1 m | Eligible? | Reported clearance | Violation |
|---|---|---|---|
| Swing, observed, z=.2 m, height=0 | Yes | .2 m | No |
| Swing, observed, z=.05 m, height=0 | Yes | .05 m | Yes |
| Stance, observed, z=-.2 m | No | NaN | Excluded |
| Terrain with no eligible samples | No evidence | Mean/min/rate NaN | Unknown |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Use one environment, two timestamps, and one foot: `foot_positions=[[[[0.,0.,0.2]],[[0.,0.,0.05]]]]`, zero terrain heights, all swing/observed masks true, `terrain_ids=[0]`, `minimum_clearance=[0.1,0.1]`, and `num_terrains=2`.

Return `clearance=[[[0.2],[0.05]]]`, `counts=[2,0]`, `mean_clearance=[0.125,NaN]`, `min_clearance=[0.05,NaN]`, and `violation_rate=[0.5,NaN]`. Terrain 1 has no evidence.

## Why this matters on a robot

An erroneous support height biases every clearance result, while counting stance feet as swing failures penalizes normal contact. Per-terrain evidence helps find fragile gait behavior, but clearance alone does not detect all collisions or establish safe walking.

## Physical contract and limits

Action targets and action scales use radians. Environmental features and their scales share declared normalized coordinates. Foot positions, terrain heights and clearance thresholds use meters; resulting normalized losses and violation rates are dimensionless. Times are already aligned within each environment. A terrain label is constant across one supplied window. No resampling, recurrent state estimation or simulator stepping occurs. Original bounded teacher/student objective or terrain diagnostic associated with perceptive locomotion; no claim to reproduce the paper's recurrent gated network, training weights or hardware performance. All fixtures are synthetic.

Source: [primary paper](https://arxiv.org/abs/2201.08117). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
