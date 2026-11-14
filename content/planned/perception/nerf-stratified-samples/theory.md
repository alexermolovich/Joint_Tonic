# Cover every part of a ray interval

## Intuition

Sampling all points independently across a ray can leave large gaps. Stratification divides the interval into bins and takes one sample in each. The supplied unit draws make the sampling reproducible without hiding randomness inside the function.

## Map unit draws to metric depths

For ray r let $n_r,f_r$ be near and far bounds in meters, with $n_r<f_r$. For S bins, define $\Delta_r=(f_r-n_r)/S$. Given unit draws $u_{ri}\in[0,1)$,

$$
z_{ri}=n_r+(i+u_{ri})\Delta_r,\qquad i=0,\ldots,S-1.
$$

Each sample belongs to $[n_r+i\Delta_r,n_r+(i+1)\Delta_r)$ in exact arithmetic. The output is already ordered by bin, so sorting is unnecessary and would obscure the association with each draw.

## Visual: three bins along a ray

| Bin | Metric interval | Unit draw | Sample |
|---|---|---:|---:|
| 0 | [1,2) m | 0 | 1m |
| 1 | [2,3) m | 0.5 | 2.5m |
| 2 | [3,4) m | 0.75 | 3.75m |

The table is a static ray trace and its text alternative. Every interval contributes one sample; a zero draw selects that bin's near endpoint.

## Physical and numerical conventions

Ray directions must have unit length for these parameters to represent meters along a ray. If a direction has length two, advancing z by one changes position by two meters. The later density integration must use metric interval lengths consistently.

Float64 rounding can make a sample extremely close to a bin boundary compare equal to it; numerical checks allow the declared tolerance. The contract uses full equal-width bins. Implementations based on jittering intervals around endpoint samples make a different discretization choice.

## Why this matters on a robot

Sparse neural-map queries can miss narrow surfaces. Stratification improves coverage but does not guarantee detection of arbitrarily thin obstacles. Record near/far policies and unit draws or RNG seeds; changing them can alter a render residual used to diagnose pose errors.

## Questions and source

Why supply draws instead of a seed? It separates deterministic geometry from RNG version and caller sampling policy. Does this produce 3D points? No; combine z with an origin and normalized direction upstream.

Source: [NeRF stratified sampling](https://arxiv.org/abs/2003.08934). This is a bounded sampling component; it does not estimate density or perform importance sampling.
