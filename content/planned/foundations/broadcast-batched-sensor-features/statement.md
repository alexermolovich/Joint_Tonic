# Broadcast Batched Sensor Features

Implement broadcast_sensor_features(sensor, context, present) -> np.ndarray.

sensor is NumPy float64(B,T,F), context float64(B,C), present bool(B,T). Bounds:1<=B<=32,0<=T<=256,1<=F,C<=64, B*T*(F+C)<=1000000. All sensor/context values finite and absolute value<=1e6, including absent timesteps. For each valid timestep concatenate sensor[b,t,:] followed by context[b,:]; absent timesteps return all zeros, including the context part. Return fresh float64(B,T,F+C). Preserve all inputs; noncontiguous arrays are valid. Invalid types/dtypes/shapes/values raise ValueError.

Each batch row represents one robot episode, T ordered synchronized sensor samples. Features are dimensionless pre-normalized channels; context is fixed episode metadata already encoded into C numerical features. This does not convert units, infer timestamps, transform frames, or infer presence from feature values.

## Worked examples

### Mask the entire absent sample
sensor[[[2],[3]]], context[[9]], present[[True,False]] returns[[[2,9],[0,0]]].

### Two different robots
sensor[[[1]],[[2]]], context[[10,11],[20,21]], present[[True],[True]] returns[[[1,10,11]],[[2,20,21]]].

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
