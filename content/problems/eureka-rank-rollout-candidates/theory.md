# Rank Reward Candidates by Rollout Evidence

## Intuition

Select a trained candidate using held-out task behavior, not the numerical scale of its training reward. Make missing evidence and observed safety violations explicit before ranking.

## Mathematical mechanism

For candidate k and trial j, let M denote observed trials, S task success, and V a safety violation. Then $$n_k=\sum_jM_{kj},\quad s_k=\frac{\sum_jM_{kj}S_{kj}}{n_k},\quad v_k=\frac{\sum_jM_{kj}V_{kj}}{n_k}.$$ Rates are NaN for n=0. A candidate is eligible when n is at least the minimum and v does not exceed the allowed rate. Sort eligible candidates lexicographically by $(-s_k,v_k,-n_k,k)$. A successful trial may also violate the safety condition; the labels are not complements.

## Visual computation trace

| Candidate | Success | Violations | With zero allowed violations |
|---|---|---|---|
| 0 | 1/2 | 0/2 | eligible |
| 1 | 2/2 | 1/2 | ineligible |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

success [[True,False],[True,True]], violations all False, valid all True, min_trials 2,max_rate 0 -> rates [.5,1], order [1,0], selected 1.

## Why this matters on a robot

A finite and well-scaled reward can still encourage the wrong behavior. Select policies with independent task and safety evidence; missing trials are not successful trials.

## Physical contract and limits

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

Source: [primary paper](https://arxiv.org/abs/2310.12931). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
