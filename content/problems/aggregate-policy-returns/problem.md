# Aggregate Mean and Worst-Case Policy Returns

Implement aggregate_policy_returns(returns, tail_fraction) -> dict.

returns is NumPy float64(P,E),1<=P<=64,1<=E<=10000,total<=200000, finite values in[-1e6,1e6]. Each row is one policy evaluated on the same ordered E scenario episodes, with comparable dimensionless undiscounted returns; higher is better. tail_fraction is a finite built-in non-bool int/float in(0,1]. Return fresh float64(P,) arrays mean, worst, lower_tail. mean is the arithmetic mean, worst the minimum. For each sorted ascending row x, let q=tail_fraction*E, k=floor(q), a=q-k. lower_tail=(sum(x[:k])+a*x[k])/q, omitting the fractional term when k=E. This fractional-mass empirical lower-tail mean is defined even when q<1. Preserve inputs; noncontiguous inputs valid. Invalid contracts raise ValueError.

This reports supplied episodic returns, not discounted-step accumulation, confidence bounds, importance weighting, policy learning, or a robust-control guarantee. The lower-tail statistic is an original evaluation extension to dynamics randomization.

## Worked examples

### Fractional tail mass
returns[[0.,2.,4.,6.]], tail_fraction0.375 returns mean[3], worst[0], lower_tail[2/3].

### Full and very small tails
For returns[[4.,-2.]], fraction1 returns mean[1], worst[-2], lower_tail[1]. With fraction0.1, mean and worst are unchanged and lower_tail[-2].

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
