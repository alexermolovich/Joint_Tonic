# Seed a Deterministic Evaluation Run

## Intuition

Re-running one failed robot episode should produce the same synthetic sensor noise even when the evaluation batch order changes. A single sequential global stream cannot provide that property when episodes are shuffled or assigned to different workers.

## Identity-derived random streams

For root seed s and episode identifier i, initialize the specified PCG64 generator from SeedSequence([s,i]). Its H×D standard-normal draw Z_i produces

$$X_{itd}=\mu_d+\sigma_d Z_{itd}.$$

Mean $\mu_d$ and nonnegative standard deviation $\sigma_d$ share the caller-declared sensor unit; $Z$ is dimensionless. $i$ identifies an episode, $t$ its ordered simulation step, and $d$ a sensor channel. Episode identity, not its batch position, determines its stream. The selected NumPy version and draw shape are part of reproducibility.

## Visual replay trace

| Evaluation batch | Output rows |
|---|---|
| IDs[7,3] | noise(7),noise(3) |
| IDs[3] | identical noise(3) |
| IDs[3,7] | noise(3),noise(7) |

The table is a static visual and text alternative. With $s=0$, $i=0$, $H=1$, $\mu=[0,0]$ and $\sigma=[1,1]$, the first row is approximately $[0.1257302211,-0.1321048633]$.

## Why this matters on a robot

Versioned seeds make simulated perturbations replayable; they do not seed external renderers, physics, GPU kernels or asynchronous hardware. Reusing an episode ID intentionally reproduces a stream, so unique IDs prevent accidental duplicate trials within one call. Global RNG mutation can contaminate unrelated evaluation components.

Sources: [PCG64](https://numpy.org/doc/2.2/reference/random/bit_generators/pcg64.html), [NumPy independent streams](https://numpy.org/doc/2.2/reference/random/parallel.html).

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
