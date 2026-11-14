# Select a Checkpoint with Offline and Rollout Gates

## Intuition

A ranking always names a winner, even when every candidate has unacceptable evidence. Gating first permits a defensible no-selection result. Coverage prevents a single lucky trial from outranking a measured policy under this teaching contract.

## Separate eligibility from preference

For candidate i, let $\ell_i$ be loss, $s_i$ successes and $n_i$ trials. Let L be the maximum loss, N the minimum trials and $p/q$ the minimum success fraction. Eligibility is

$$
e_i=\mathbf1[\ell_i\le L]\mathbf1[n_i\ge N]\mathbf1[s_i q\ge p n_i].
$$

L and loss share one dimensionless upstream definition. Counts, p and q are integers; $q>0$ and $N\ge1$. Exact cross-products avoid rounding a threshold percentage. Zero-trial rows fail coverage before any division.

Among eligible candidates, prefer higher $s_i/n_i$, then lower $\ell_i$, then the lexicographically smaller ID. No eligible rows means no selected checkpoint.

## Visual: gates explain the first example

| Checkpoint | Loss<=0.3 | Trials>=10 | Success>=4/5 | Eligible |
|---|---|---|---|---|
| fit | yes | yes | yes, equality | yes |
| risky | no | yes | yes | no |
| short | yes | no | yes | no |

The table is a static gate trace and text alternative. The highest raw success rate does not bypass missing coverage.

## Why this matters on a robot

Low imitation loss can coexist with poor closed-loop recovery, while impressive short evaluations can be luck. Requiring multiple forms of evidence makes the selection rule reviewable. Thresholds themselves need a separate application-specific justification; passing them is not a physical safety certificate.

Repeatedly tuning candidates against the same final test set also creates evaluation leakage. This function records a choice from supplied evidence and cannot fix that experiment design.

## Questions

1. Why is None a meaningful output?
2. Why must selection happen after the eligibility gates?

## Sources and prerequisites

robomimic motivates comparing offline objectives with rollout behavior. These explicit thresholds and deterministic selection rules are an original teaching policy, not a claim about the paper's exact checkpoint selection implementation. [Primary source](https://arxiv.org/abs/2108.03298), Stopping criteria and policy selection from offline demonstrations. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

