# Hints

1. Broadcast the timestep mask over action channels.
2. Compute variance with exp(log_variance), not exp(2*log_variance).
3. Sum latent dimensions and average batch items; reconstruction uses a different denominator.
