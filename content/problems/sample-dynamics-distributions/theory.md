# Theory: randomize physical assumptions with a replayable contract

## Intuition

A policy trained with one perfectly known object mass may behave poorly when the real object is heavier. Sampling a family of physical configurations exposes training to such variation. The sampling rule is part of the experiment: changing units, parameter order, or reset timing creates a different distribution.

This component transforms supplied unit draws. Recording those draws or the upstream generator's seed makes it possible to reproduce a configuration without embedding a simulator or random-number implementation into the exercise.

## Positive scales belong on a declared distribution

Let $U\in[0,1)^{B\times4}$ contain B episode rows, ordered mass, friction, delay, gain. For a positive parameter with lower and upper bounds $a,b$, define

$$
z_i=\exp\!\left(\log a+U_{ij}(\log b-\log a)\right).
$$

Here $j$ is the parameter's designated column. The implementation uses numerical values in the declared unit. Equivalently, the dimensionally clear expression is

$$
z_i=a\left(\frac{b}{a}\right)^{U_{ij}}.
$$

The ratio is dimensionless; $z_i$ has the units of $a$. At unit draw 0.5, the value is $\sqrt{ab}$, the geometric mean. If upstream draws are uniform, equal-width intervals in log space receive equal probability. This differs from a linear uniform distribution and is useful when proportional changes are the intended uncertainty.

Mass is in kilograms, friction is a dimensionless coefficient, and gain is a dimensionless multiplier of an existing baseline controller gain. This function does not infer new absolute gains or update a body's inertia tensor.

## Integer delay and reset semantics

Let $l,h$ be inclusive nonnegative tick bounds and $M=h-l+1$ the number of allowed tick values. For delay column 2, define

$$
d_i=l+\lfloor M U_{i2}\rfloor,\qquad
\tau_i=d_i\Delta t.
$$

The output $d_i$ is int64 control ticks; $\Delta t$ is the supplied dt_s in seconds per tick, and $\tau_i$ is delay_s in seconds. Half-open unit draws ensure that a delay never exceeds $h$. Each integer occupies an interval of unit-draw width $1/M$. Parameters are fixed for an episode.

The paper uses a different action-timestep randomization process. Our fixed integer delay is a deliberately bounded teaching extension, not a transcription of that process.

## Visual and worked values

~~~mermaid
flowchart LR
  U["U: B by 4 supplied draws"] --> M["Column0: log mass bounds"]
  U --> F["Column1: log friction bounds"]
  U --> D["Column2: integer delay buckets"]
  U --> G["Column3: log gain bounds"]
  D --> S["delay_seconds = ticks times dt_s"]
~~~

**Text alternative:** each row supplies separate draws for mass, friction, delay, and gain. Three columns use positive log ranges; delay uses integer buckets and then a seconds conversion. The diagram is static.

For a row of four 0.5 values and example 1's bounds:

| Output | Calculation | Value |
|---|---|---|
| mass_kg | sqrt(1×9) | 3 kg |
| friction | sqrt(0.25×1) | 0.5 |
| delay_ticks | floor(4×0.5) | 2 ticks |
| gain_scale | sqrt(0.5×2) | 1 |
| delay_s | 2×0.01 | 0.02 s |

## Why this matters on a robot

Replayable distributions support failure analysis across mass, contact, and actuation assumptions. They do not establish a safe operating envelope by themselves. Independent scalar draws can miss correlated real-world parameters, and a full rigid-body model also needs a physically valid inertia tensor. Resampling mass every physics step would train on a different, usually unintended process.

The source motivates dynamics variation and log-sampled parameters; our synthetic ranges and delay contract are explicit deviations. [Dynamics Randomization primary source](https://arxiv.org/abs/1710.06537).

## Questions

1. Why is the midpoint mass 3 kg instead of 5 kg for bounds 1 and 9?
2. Why must a trace distinguish control ticks from simulator substeps?

Prerequisite: recognize mass, contact friction, and delayed actuation as physical model assumptions. No simulator installation is required for this planned function.
