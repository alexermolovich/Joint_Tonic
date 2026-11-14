# Build a Seeded Visual Randomization Sampler

## Intuition

Replaying a failed visual condition requires its randomization settings and exact stream. Draw the factors once per scenario instead of scattering implicit random calls across rendering code.

## Transform one reproducible uniform stream

For u in[0,1), a continuous interval maps by

$$x=l+u(h-l).$$

A discrete inclusive integer interval maps by $n=l+\lfloor u(h-l+1)\rfloor$. Texture choice uses the same binning over ordered IDs. Four columns have fixed factor meanings. A degenerate continuous interval stays fixed but still consumes its column; later factors therefore remain reproducible.

## Visual: one scenario's four factors

| Uniform column | Meaning | Mapping |
|---:|---|---|
| 0 | texture | ordered categorical index |
| 1 | brightness | exposure multiplier interval |
| 2 | yaw | world+z radians interval |
| 3 | distractors | inclusive integer count |

This table is the original sampler graph and text alternative. Factor sampling is independent in this exercise; physical rendering may introduce additional correlations.

## Why this matters on a robot

A broad randomization range may erase useful visual evidence or create implausible views. Recorded samples support diagnosis, but they do not prove sim-to-real transfer. Keep camera coordinate conventions and seed/runtime versions with the fixture.

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
