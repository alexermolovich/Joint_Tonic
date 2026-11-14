# Report Policy Update Clip Fractions

## Intuition

A probability ratio outside the clipping interval does not always change PPO’s objective. Separate raw ratio excursions from the signed cases where the clipped branch actually limits improvement, then report a likelihood-based change diagnostic.

## Mathematical mechanism

With $r=\exp(\ell)$ and $\ell=\log\pi_{new}-\log\pi_{old}$, $$c_{ratio}=\mathbf1[r<1-\epsilon\ \lor\ r>1+\epsilon],\quad c_{active}=\mathbf1[(A>0\land r>1+\epsilon)\lor(A<0\land r<1-\epsilon)].$$ Report their valid-entry averages. Also report $\widehat K=\operatorname{mean}_{valid}(\exp(\ell)-1-\ell)$, an empirical nonnegative surrogate; it is not an exact distribution-wide KL divergence or safety bound.

## Visual computation trace

| Ratio | Advantage | Outside interval | Limits objective |
|---|---|---|---|
| 1.5 | +1 | yes | yes |
| 1.5 | -1 | yes | no |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

ratios[1.5,.5],advantages[1,-1],epsilon.2 gives bothfractions1, KLmean((.5-log1.5)+(-.5-log.5))=-.5log(.75).

## Why this matters on a robot

A high ratio excursion rate and a low active-clipping rate describe different updates. Treating either as proof of bounded policy change can hide risky robot behavior. This diagnostic must use the same action likelihood convention as the policy loss.

## Physical contract and limits

Log densities and ratios are dimensionless; advantage/value/return terms use the caller-fixed reward units. Ordered transition indices at a fixed caller-declared control interval; terminal events differ from time limits. Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.

Source: [primary paper](https://arxiv.org/abs/1707.06347). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
