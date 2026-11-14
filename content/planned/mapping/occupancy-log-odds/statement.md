# Update Occupancy Belief from Range Evidence

**Status: planned; no runnable implementation yet.**

A range sensor repeatedly observes a map cell. Update its occupancy belief without treating every reading as an independent new map.

## Contract

Planned function: update_occupancy(log_odds, inverse_probability, prior_probability, limits).

The current log odds are a finite scalar belief. The inverse probability is the inverse sensor model's occupancy probability for this cell given the latest observation; the prior probability is the prior used by that model. Both probabilities lie strictly between zero and one. Limits contain finite increasing log-odds bounds.

Return the clamped new log odds and corresponding occupancy probability. Add the inverse-model log odds and subtract the model prior's log odds exactly once per observation. Do not interpret an unobserved cell as free: the caller sends no update when there is no evidence.

## Assumptions

The cell belongs to a fixed metric map, observations refer to the same cell, and the teaching model combines conditionally independent evidence. Ray tracing, moving-object handling, and coordinate conversion are separate components.

## Assessment plan

Use hit/free sequences, non-0.5 priors, saturation, and invalid probabilities. See [examples.md](examples.md). This planned folder has no implementation or test runner yet.

