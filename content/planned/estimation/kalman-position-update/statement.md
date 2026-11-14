# Fuse a Position Measurement with a Kalman Update

**Status: planned; no runnable implementation yet.**

A mobile robot has a predicted one-axis world position and a noisy independent position measurement. Compute one scalar Kalman measurement update and report the evidence behind it.

## Contract

Planned function: update_position(mean, variance, measurement, measurement_variance).

All four inputs are finite real scalars. Position quantities are meters in the same world axis and timestamp. Prior variance is nonnegative; measurement variance is strictly positive. Noise is unbiased and independent. Return {mean, variance, innovation, gain} using the scalar identity-observation model. Preserve the prior as input data.

Use innovation = measurement - mean; gain is prior variance divided by total variance. Use the Joseph-form scalar posterior variance, $(1-K)^2P+K^2R$, so the uncertainty calculation expresses both remaining sources. Reject invalid variance and nonfinite input. No motion prediction or outlier rejection is included.

## Learning outcome

Explain why the noisier source receives less influence, and distinguish the measurement residual from the corrected position. Read the two worked cases in [examples.md](examples.md).

## Assessment plan

Check exact hand cases, zero prior variance, highly uncertain measurements, nonnegative posterior variance, and input validation. Comparisons use declared floating tolerance, not string equality. This folder is planned and does not yet provide a runnable evaluator.

