# Detect Paused or Corrupted Action Segments

## Intuition

Zero commands may indicate an intentional pause or a disconnected stream. Keep observation corruption separate and require a contiguous duration before labelling an interval as paused.

## Formal model

Let $c_t$ mark corrupted evidence and command vector $u_t\in\mathbb R^D$ use rad/s. With deadband $\delta$ in rad/s, a pause candidate satisfies $\neg c_t$ and $\|u_t\|_\infty\le\delta$. A maximal run $[a, b)$ qualifies when
$$b-a\ge m,\qquad t_{b-1}-t_a\ge\Delta_{\min}.$$
Times are integer nanoseconds, $m$ is a sample count, and $\Delta_{\min}$ is the required observed endpoint duration. This does not assume a nominal sample period or fill gaps between timestamps.

## Worked state and shape trace

```text
commands0,0,1,0 -> candidate T, T, F, T -> runs[0,2),[3,4); min2samples retainsfirst, endpointduration10ns.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Long zero-command segments can dominate imitation datasets. Flagging them supports curation but cannot decide whether a human intentionally paused, a controller held position, or a network failed.

## Source and scope

Original bounded component inspired by [2018-roboturk](https://arxiv.org/abs/1811.02790). It does not reproduce the full paper or establish hardware safety or data-use authorization.
