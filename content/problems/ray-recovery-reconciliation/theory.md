# Recover Failed Worker Tasks Idempotently

## Intuition

Collapse duplicated delivery before planning a retry. A successful immutable result stays committed even if a later attempt failed; a task with external side effects cannot automatically be replayed.

## Formal model

For task $i$, let $A_i$ be observed attempt numbers and $H_i$ the set of successful output digests. Require $|H_i|\le1$. When no result is committed and replay is allowed, the next attempt is
$$r_i=1+\max(A_i\cup\{0\}).$$
A configured maximum bounds retries; success takes precedence over later failure. These are deterministic state-machine rules for supplied evidence, not a proof of exactly-once robot actions.

## Worked state and shape trace

```text
a:failed1 -> retry2; b:no evidence -> pending1; success(hash h)+laterfailure -> committed h.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Retrying a pure dataset transform can be safe; repeating a grasp or calibration write may not be. The replay_safe flag is supplied evidence, not a hardware safety check.

## Source and scope

Original bounded component inspired by [2017-ray](https://arxiv.org/abs/1712.05889). It does not reproduce the full paper or establish hardware safety or data-use authorization.
