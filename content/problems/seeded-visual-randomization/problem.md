# Build a Seeded Visual Randomization Sampler

Implement sample_visual_scenarios(count, seed, textures, brightness, yaw, distractors) -> dict.

count and seed are built-in non-bool ints in[0,10000] and[0,2**32-1]. textures is a Python list of1–64 unique ASCII IDs[a-z][a-z0-9_-]{0,63}, whose order is meaningful. brightness and yaw are tuples(lo,hi) of finite built-in non-bool numbers, lo<=hi: brightness in[0,10] is a dimensionless exposure multiplier, yaw in[-pi,pi] is camera yaw radians about caller's world+z axis with no angle wrapping. distractors is a tuple of built-in ints0<=lo<=hi<=100, a count not a physical density.

Use an independent np.random.Generator(np.random.PCG64(seed)); draw exactly U=rng.random((count,4)). In column order select texture index floor(u0*len(textures)), brightness=lo+u1*(hi-lo), yaw=lo+u2*(hi-lo), distractor count=lo+floor(u3*(hi-lo+1)). Return dict texture:list[str], brightness:float64(count,), yaw:float64(count,), distractors:int64(count,), all independent storage. No global RNG use, input mutation, rendering, robot movement, or label change. count0 returns correctly typed empty outputs but validates all settings. Invalid contracts raise ValueError.

## Worked examples

### Four factors from seed0
For count1,seed0,textures["a","b"],brightness(1,2),yaw(-1,1),distractors(0,2), the result is texture["b"], brightness approximately[1.2697867138], yaw approximately[-0.9180529521], distractors[0].

### Fixed factors still have valid outputs
For count2,seed7,textures["only"],brightness(2,2),yaw(0,0),distractors(3,3), return texture["only","only"], brightness[2,2], yaw[0,0], distractors[3,3].

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
