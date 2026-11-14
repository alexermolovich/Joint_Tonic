# Worked examples

### Interleaved trajectories share their scene assignment

~~~python
split_trajectories_by_scene(
    ["ep_a","ep_b","ep_c","ep_d"],
    ["kitchen","office","kitchen","warehouse"],5000,7)
# {"train":["ep_a","ep_c"], "validation":["ep_b","ep_d"]}
~~~

For seed7 the buckets are kitchen9538, office2001 and warehouse925. Both kitchen trajectories remain in train even though they are separated in input order.

### A split threshold is not a target count

~~~python
split_trajectories_by_scene(
    ["trial_a","trial_b"],["office","office"],2001,7)
# {"train":["trial_a","trial_b"], "validation":[]}
~~~

The office bucket equals2001; strict inequality puts both trajectories in train. At threshold2002 both would move to validation together. Splitting two trajectories from one scene into opposite sets would violate this contract.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

