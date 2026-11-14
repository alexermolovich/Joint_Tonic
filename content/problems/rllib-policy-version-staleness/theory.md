# Track Policy Version Staleness

## Intuition

A fast rollout worker can still send data produced by an obsolete policy. Count how much usable evidence each version contributes instead of averaging worker flags.

## Formal model

Learner version $v$ and sample-batch version $v_i$ give $\ell_i=v-v_i$. For sample count $n_i$ and allowed lag $L$,
$$a_i=\mathbf1[0\le\ell_i\le L],\qquad N_{\rm accepted}=\sum_i n_i a_i.$$
The reported mean includes nonfuture rows: $\bar\ell=\sum_{\ell_i\ge0}n_i\ell_i/\sum_{\ell_i\ge0}n_i$, undefined(NaN) when the denominator is zero. All version/count quantities are dimensionless; no timestamp conversion is implied.

## Worked state and shape trace

```text
versions10,7,12 at learner10 -> lags0,3,-2 -> accept only current row underlag2; sample counts2,6,4 remain visible.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Accepting future-version evidence can hide mixed learner runs. A small version lag is not proof that off-policy samples are valid for every learning algorithm.

## Source and scope

Original bounded component inspired by [2017-rllib](https://arxiv.org/abs/1712.09381). It does not reproduce the full paper or establish hardware safety or data-use authorization.
