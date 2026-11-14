# Aggregate Weighted Learner Gradients

## Contract

`aggregate_learner_gradients(mean_gradients, sample_counts) -> dict`. mean_gradients is NumPy float32/float64(P, D),0<=P<=4096,1<=D<=256, at most 10^6 entries; all values finite with abs<=10^6, including zero-count rows. sample_counts is NumPy int64(P,),0..10^6. Each gradient is the mean over that worker's valid samples, not a gradient sum. Return mean:float64(D,), norm:Python float L2 norm of the combined mean, total_samples:Python int, has_samples:Python bool. With positive total, mean=sum(n_i*g_i)/sum(n_i); with zero total return a zero vector, norm=0, has_samples=False. Preserve inputs and support noncontiguous arrays. No optimizer step, clipping or gradient transport occurs. Work O(PD).

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

mean_gradients=[[1],[3]], counts[2,6] gives mean[2.5], norm=2.5, total_samples=8, has_samples=True.

mean_gradients=[[100,-20]], counts[0] gives mean[0,0], norm=0, total_samples=0, has_samples=False. A nonfinite ignored row is still invalid evidence.

## Source and scope

Original bounded component inspired by [2017-rllib](https://arxiv.org/abs/1712.09381). It does not reproduce the full paper or establish hardware safety or data-use authorization.
