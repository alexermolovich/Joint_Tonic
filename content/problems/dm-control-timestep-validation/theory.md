# Validate a Continuous-Control Time Step

## Intuition

A simulator transition carries both an episode-boundary marker and a bootstrap discount. They answer different questions: a time limit can end collection while preserving the value estimate of the final state. FIRST is different again because no preceding action produced its reward.

## Mathematics and physical contract

The step type $s\in\{0,1,2\}$ denotes FIRST, MID, and LAST. For FIRST, reward $r$ and discount $d$ are undefined and represented by None. Otherwise require finite reward and
$$0\le d\le1.$$
The bootstrap contribution of next-state value $V(o')$ is $dV(o')$. LAST with $d=0$ represents no continuation value; LAST with $d>0$ may represent truncation. Observation $o\in\mathbb R^D$ is a caller-defined feature vector whose per-column units and frame remain unchanged. This schema checker does not infer termination causes or validate a whole sequence.

## Worked pipeline and shape trace

```text
LAST, reward1, discount1, observation[0] -> []
FIRST, reward0, missing discount, extra key ->
[invalid:reward, missing:discount, unexpected:extra]
outer fields -> independent structural checks -> conditional reward/discount checks
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

Confusing time-limit truncation with a physically terminal event changes value targets. Separately, a valid observation shape does not prove the sensors are calibrated or synchronized.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2018-deepmind-control-suite](https://github.com/google-deepmind/dm_env/blob/master/dm_env/_environment.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
