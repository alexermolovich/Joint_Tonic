# Solution explanation

Promote gradients to float64 before multiplying by sample counts. Sum weighted gradients over workers and divide by total valid samples. With zero total, return a typed zero vector plus has_samples=False. Compute the norm of the combined mean, not the mean of worker norms. Work/storage O(PD) for the straightforward vectorized implementation.
