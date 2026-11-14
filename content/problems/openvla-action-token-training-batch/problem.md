# Build a VLA Action-Token Training Batch

A robot policy should learn action tokens without being asked to reconstruct its instruction as part of this objective. Preserve the full prompt as context, supervise only actions and EOS, and distinguish padding from tokens that happen to share ordinary values.

## Contract

prompts/actions nonempty aligned Python lists of B integer vectors,1<=B<=32. Each prompt length1..256; each action length1..64. vocab_size integer scalar4..1000000, pad_id/eos_id distinct integer scalars0..vocab_size-1. Source token IDs in vocabulary and neither special ID. For each row concatenate prompt, actions, EOS; right-pad to longest row. Return input_ids int64(B,L), labels int64(B,L), attention_mask bool(B,L), lengths int64(B). Labels copy ONLY action tokens and final EOS; prompt and padding labels=-100. Labels are aligned with input positions, NOT shifted: a causal language-model loss shifts logits/labels externally. Do not insert BOS or truncate.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized actions and token features are dimensionless; physical calibration is supplied upstream. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.


## Example 1

prompts=[[7],[6,7]], actions=[[8],[9]], pad0,eos1,vocab10 gives inputs[[7,8,1,0],[6,7,9,1]], labels[[-100,8,1,-100],[-100,-100,9,1]], lengths[3,4].

## Example 2

prompt[[2]], actions[[3,4]], pad0,eos1,vocab5 gives input[[2,3,4,1]], labels[[-100,3,4,1]], all attention entriesTrue.
