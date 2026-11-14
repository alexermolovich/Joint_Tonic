# Construct Relative Pose Measurements from Local Odometry

Implement `relative_odometry(poses, times, edges)`.

`relative_odometry(poses, times, edges)` poses(N,4,4),1<=N<=8192 are body-to-local-world transforms, translations meters; times(N) seconds strictly increasing, adjacent spacing>=1e-6; edges(E,2),0<=E<=32768, each 0<=i<j<N; duplicates allowed, preserve edge order.

Return transforms(E,4,4)=Ti^-1 Tj, durations(E)=tj-ti, speeds(E)=norm(relative_translation) / duration in m/s.

Relative transform maps body-j coordinates into body-i; speeds are chord speed, not path speed.

No scale estimation, time interpolation or pose optimization.

Example: local poses identity at x=0 andx2, times[0,2],edge[0,1]=>relative translation[2,0,0],duration 2,speed 1.

Example: Ri=Rz90 at origin, Rj=I with world translation[1,0,0]=>relative rotationRz-90,translation[0,-1,0].

Empty edges preserves output shapes.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Identity rotations, local positions x=0 and x=2 meters at times 0 and 2 seconds, edge [0,1]: output translation [2,0,0], duration 2, chord speed 1 m/s.
2. First pose rotates 90 degrees about z at the origin; second has identity rotation and world position [1,0,0].

The relative rotation is -90 degrees about z and translation [0,-1,0].

## Source and scope

[Primary source](https://arxiv.org/abs/1901.03642).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
