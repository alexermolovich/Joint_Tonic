# Aggregate Seeded Benchmark Returns

## Intuition

A training seed with many recorded evaluation episodes should not silently receive more weight than another seed. First average episodes within a task/seed cell, then average observed seeds within a task, then average tasks. Keep missing cells visible.

## Mathematics and physical contract

For task $m$ and training seed $s$, let $E_{ms}$ be its evaluation episode indices and $G_e$ the supplied return. Define $n_{ms}=|E_{ms}|$ and, when $n_{ms}>0$,
$$\mu_{ms}=\frac{1}{n_{ms}}\sum_{e\in E_{ms}}G_e,\qquad \mu_m=\frac{1}{|S_m|}\sum_{s\in S_m}\mu_{ms},\qquad \mu=\frac1M\sum_m\mu_m.$$
$S_m$ contains only measured seeds for task $m$. Missing cells are NaN, not zero. Returns must share a declared reward and horizon convention; these means retain the return unit. Task and seed IDs are exact nonnegative integers, not numerical coordinates. Empty evidence produces NaN overall.

## Worked pipeline and shape trace

```text
task0/seed1 episodes[0,2] -> mean1, count2
task0/seed2 episode[9] -> mean9, count1 -> task0 mean5
task1/seed1 episode[4] -> mean4, count1 -> task1 mean4
missing task1/seed2 -> NaN; overall(5+4)/2=4.5
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Uneven robot evaluation effort can bias a pooled return average. This summary exposes those denominators but does not correct a biased scene selection or estimate uncertainty across training seeds.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2018-deepmind-control-suite](https://arxiv.org/abs/1801.00690). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
