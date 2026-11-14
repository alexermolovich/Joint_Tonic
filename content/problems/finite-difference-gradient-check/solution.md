# Solution explanation

Create independent plus/minus copies for each calibration coordinate and evaluate exactly the summed half-squared residual loss. Use the symmetric bounded denominator for comparison; do not substitute the supplied analytic gradient. Work O(MD²), extra storage O(M+D). Finite differences may need an appropriately selected step and tolerance.
