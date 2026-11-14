# Compute Confidence Intervals Across Robot Episodes

Implement episode_mean_interval(episodes, critical) -> dict.

episodes is NumPy float64(E,M),2<=E<=10000,1<=M<=32,total<=200000; finite abs<=1e6. Each row is one independent robot episode summary; each column a metric in its own fixed declared unit. critical is finite built-in non-bool int/float0..100, a caller-selected two-sided critical multiplier. Compute per-column sample mean, sample variance with denominator E-1, standard_error=sqrt(variance/E), interval[mean-critical*standard_error,mean+critical*standard_error]. Return mean/standard_error float64(M,), interval float64(M,2), new independent arrays; preserve inputs, noncontiguous valid. Invalid contracts raise ValueError. Do not clip bounds or infer a success-rate interpretation.

This arithmetic builds a mean interval using a supplied multiplier. For normally distributed independent episode summaries, a matching Student-t critical value can provide the selected confidence level; the function does not compute that quantile or guarantee coverage for arbitrary distributions. Correlated timesteps from one rollout are not independent episodes. Different metric columns are summarized separately, not pooled.

## Worked examples

### Three independent episode summaries
episodes[[1],[3],[5]], critical2 returns mean[3], standard_error[1.1547005384], interval approximately[[0.6905989232,5.3094010768]].

### No observed between-episode variation
episodes[[2,7],[2,7]], critical3 returns mean[2,7], standard_error[0,0], interval[[2,2],[7,7]].

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
