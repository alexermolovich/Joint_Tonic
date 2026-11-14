# Evaluation and failure analysis

The isolated worker checks collected return traces, parameter updates, clip diagnostics and held-out deterministic outcomes using fixed supplied noise. It also checks no-update and empty-learning-signal cases. Passing means the declared pipeline is implemented correctly; it does not require claiming the policy always improves.

Report training return and held-out final position error separately. Training return includes the exploration noise and action penalty; evaluation uses mean actions and independent target positions. A rising training return can coexist with asymmetric held-out error because the linear policy shares one bias across goals.

Compare at least one positive-only training-goal set with symmetric held-out targets. Inspect whether the learned bias helps one direction while hurting the other. Keep the iteration budget, supplied noise, reward scale and target sets fixed when comparing runs.
