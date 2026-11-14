# Split Robot Trajectories Without Scene Leakage

Implement split_trajectories_by_scene(episode_ids, scene_ids, validation_buckets, seed) -> dict[str,list[str]].

episode_ids and scene_ids are Python lists of equal length 0–100,000. Each element is a string matching ASCII [a-z][a-z0-9_-]{0,63}. Episode IDs must be unique; repeated scene IDs are expected. A scene ID means one shared evaluation environment under the upstream data policy; this function does not infer scene identity from images or poses.

validation_buckets is a built-in non-bool int in [0,10000]. seed is a built-in non-bool int in [0,2**32-1]. For each distinct scene:
1. Form the exact string str(seed) + "\0" + scene_id, where "\0" is one zero-valued Unicode character (not a slash and zero).
2. Encode that string as UTF-8 and compute SHA-256.
3. Interpret the first 8 digest bytes as one unsigned big-endian integer; reduce modulo10000.
4. Assign the entire scene to validation if its bucket is strictly less than validation_buckets; otherwise assign it to train.

Return exactly {"train": [...], "validation": [...]}, with episode IDs in their original input order within each partition. Every episode occurs once and no scene occurs in both partitions. Empty inputs return two empty lists. The threshold0 means all train;10000 means all validation. Inputs remain unchanged and output lists are fresh and independent.

Malformed types, IDs, duplicate episodes, length disagreement or out-of-bound numbers raise ValueError. There is no RNG, Python hash(), timestamp sorting, approximate split-size guarantee or automatic class balancing. New episodes for an existing scene retain its assignment when seed and threshold are unchanged.

## Worked examples

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

## Source and scope

robomimic motivates careful evaluation of offline robot demonstrations. Grouping by supplied scene identity and the exact SHA-256 bucket protocol are original teaching choices, not a split algorithm claimed by the paper. [Primary source](https://arxiv.org/abs/2108.03298).

