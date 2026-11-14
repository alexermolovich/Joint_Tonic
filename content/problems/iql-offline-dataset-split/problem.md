# Validate an Offline Dataset Split

A robot episode can contain many correlated transitions. Keeping its records within one data split avoids evaluating on the same rollout used for fitting; including source identity prevents unrelated datasets with matching local episode numbers from colliding.

## Contract

episode_ids, split_ids and source_ids are integer vectors(N,),0<=N<=100000. Episode/source IDs lie in[0,1e6]; split IDs are0train,1validation,2test. Episode identity is the pair(source_id,episode_id). Return a dict counts:int64(3,) record counts, leakage_pairs:int64(K,2) sorted lexicographically by source then episode for identities appearing in multiple splits, missing_splits:int64(J,) ascending absent split IDs, and valid:Python bool true only with no leakage and all three splits present. Repeated records within one split are allowed. Empty input yields zero counts, leakage shape(0,2), missing[0,1,2], validFalse. This checks declared identity, not image similarity or time ordering.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward and value share fixed reward units; log densities and entropy are in natural-log units; normalized action coordinates are dimensionless. One aligned transition per record; true termination differs from time-limit truncation. No physical simulator runs. Original bounded component using supplied policy/value data. No online learning, external model weights or full-paper benchmark reproduction.


## Example 1

episodes[1,1,2], sources[0,0,0], splits[0,1,2] returns counts[1,1,1], leakage_pairs[[0,1]], no missing splits, validFalse.

## Example 2

episodes[1,1,1], sources[0,1,2], splits[0,1,2] have three distinct identities and return validTrue.
