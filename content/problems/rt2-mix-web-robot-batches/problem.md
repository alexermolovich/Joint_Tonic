# Mix Web and Robot Batches at a Target Ratio

Co-training mixes robot examples with web supervision, but a ratio alone does not specify finite batch rounding or what happens when a source is small. Make those decisions explicit so training is reproducible.

## Contract

`mix_web_robot(web_ids,robot_ids,robot_fraction,batch_size)` receives nonnegative integer ID vectors(W,),(R,), lengths0..10000; scalar robot_fraction in[0,1]; integer batch_size1..4096. Set robot quota=floor(batch_size*robot_fraction+0.5), web quota=remainder. Any source with positive quota must be nonempty. Return dict source:int64(B,) where1robot/0web and ids:int64(B,). Emit all robot rows then all web rows, cycling each source’s IDs from index0 with replacement. Duplicate IDs allowed; no random draw or shuffling.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Dataset IDs/source labels and ratios are dimensionless; no common raw action space is assumed. This is one training batch assembly; per-source sequence order remains external. Original deterministic co-training mixer inspired by RT-2. Half-up rounding, source order and cycling are teaching rules rather than the paper’s training sampler.


## Example 1

web_ids=[2], robot_ids=[8,9], robot_fraction=0.5, batch_size=5 returns source=[1,1,1,0,0], ids=[8,9,8,2,2].

## Example 2

web_ids=[4,5], robot_ids=empty int vector, robot_fraction=0, batch_size=3 returns source=[0,0,0], ids=[4,5,4]. An unused empty source is valid.
