# Seed a Deterministic Evaluation Run

Implement seeded_episode_noise(episode_ids, root_seed, horizon, mean, std) -> np.ndarray.

episode_ids is NumPy int64(E,),0<=E<=256, unique IDs0..2**32-1. root_seed built-in non-bool int0..2**32-1; horizon built-in non-bool int0..256. mean/std NumPy float64(D,),1<=D<=32, mean finite abs<=1000,std finite0..1000. Total E*horizon*D<=1000000. For each episode ID i independently construct np.random.Generator(np.random.PCG64(np.random.SeedSequence([root_seed,int(i)]))). Draw exactly standard_normal((horizon,D)) then multiply by std and add mean. Return fresh float64(E,horizon,D) in supplied ID order, preserving inputs and legacy global np.random state. Noncontiguous inputs valid; zero episodes/horizon returns correct shape while validating all settings. Invalid contracts raise ValueError.

Each feature channel uses one caller-declared sensor unit shared by mean/std and output; channels may differ in units. Noise samples are independent synthetic perturbations at fixed caller-defined simulation timesteps. Pin NumPy2.2.4 for this normal-draw replay contract; no claim across arbitrary library versions. Reordering or splitting episode IDs must preserve each episode's generated values. No simulator state is seeded here.

## Worked examples

### Known local stream
IDs[0], root_seed0,horizon1,mean[0,0],std[1,1] returns approximately[[[0.1257302211,-0.1321048633]]].

### Zero noise scale
IDs[4,8], root_seed9,horizon2,mean[3],std[0] returns[[[3],[3]],[[3],[3]]].

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
