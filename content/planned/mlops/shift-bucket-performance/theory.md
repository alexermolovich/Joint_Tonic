# Measure Performance Across Shift Buckets

## Intuition

A good overall average can hide a failure under glare or an unusual camera pose. Keeping each shift bucket's count, mean and worst observed loss makes missing and fragile regions visible.

## Conditional empirical risk

For bucket b, let I_b contain its scenario indices and n_b its size. With normalized dimensionless loss e_i,

$$\widehat R_b=\frac1{n_b}\sum_{i\in I_b}e_i,\qquad W_b=\max_{i\in I_b}e_i.$$

Both metrics are undefined for n_b=0 and returned as NaN, not zero. The worst observed loss is not a bound on unseen scenes.

## Visual: keep missing slices visible

| Bucket | Losses | Count | Mean | Worst |
|---:|---|---:|---:|---:|
| 0 | 1,3 | 2 | 2 | 3 |
| 1 | 9 | 1 | 9 | 9 |
| 2 | none | 0 | NaN | NaN |

This original table is the slice comparison and text alternative. Bucket2 must not look like perfect zero error simply because it was untested.

## Why this matters on a robot

A rare visual condition may matter more than its dataset frequency. Aggregating comparable metrics helps isolate it, but counts and scenario provenance still govern confidence. A common failure is silently dropping empty buckets from a release report.

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
