# Tiny PPO controller integration

A scalar joint starts at zero and must approach a supplied target. A linear Gaussian policy chooses velocity commands; an explicit integrator advances the synthetic state. You will collect trajectories, compute terminal discounted returns, normalize advantages, take repeated clipped-surrogate updates and evaluate held-out goals.

```text
training goals + supplied noise -> fixed-policy rollouts
  -> terminal returns -> normalized advantages
  -> frozen behavior likelihoods + PPO epochs
  -> updated controller -> separate held-out goal evaluation
```

Each arrow is a data dependency, and the written sequence is also the text alternative to the pipeline. No animation is required.

This is a real bounded parameter-update loop on a deliberately small environment. It does not include neural perception, a learned critic, MuJoCo, contact dynamics, real-hardware execution or PPO's published locomotion experiments. The reward, dynamics, Gaussian scale, norm clipping and parameter projection are fully specified teaching choices. Read the integration contract before composing the atomic components.
