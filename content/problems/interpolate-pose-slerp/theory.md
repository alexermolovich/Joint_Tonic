# Interpolate a Pose with SLERP

## Intuition

Blending rotation matrices entrywise usually destroys orthogonality. Unit quaternions lie on a sphere; following its shorter arc interpolates orientation without collapsing the rotation representation.

## Mathematics and physical meaning

Normalize scalar-first quaternions $a,b\in\mathbb R^4$ and flip $b$ when $a^\top b<0$. Let $d=\operatorname{clip}(a^\top b,-1,1)$, $\theta=\arccos d$, and interpolation fraction $u\in[0,1]$. For $d\le0.9995$,
$$q(u)=\frac{\sin((1-u)\theta)}{\sin\theta}a+\frac{\sin(u\theta)}{\sin\theta}b.$$
When the endpoints are nearly equal, use $q(u)=\operatorname{normalize}((1-u)a+ub)$ to avoid dividing by a tiny sine. Normalize the final result in both branches. Translation is $p(u)=(1-u)p_0+up_1$, in metres. Quaternion angular distance is half the corresponding physical rotation angle.

## Visual trace

| Fraction | Position from [0,0,0] to [2,0,0] | Rotation identity to +180° z |
|---|---|---|
| 0 | [0,0,0] | 0° |
| 0.5 | [1,0,0] | 90° |
| 1 | [2,0,0] | 180° |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `p0=[0,0,0], q0=[1,0,0,0], p1=[2,0,0], q1=[0,0,0,1], fraction=0.5` → position `[1,0,0]`, quaternion `[sqrt(0.5),0,0,sqrt(0.5)]`.
2. Same positions, `q0=[2,0,0,0], q1=[-3,0,0,0], fraction=0.5` → position `[1,0,0]`, quaternion `[1,0,0,0]`; opposite signs describe the same orientation.

## Why this matters on a robot

Quaternion signs can flip between sensor frames without any physical rotation. Failing to correct that sign can interpolate along the wrong path or divide by zero. This pose interpolation does not respect obstacles or joint limits.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
