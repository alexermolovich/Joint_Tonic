# Parse and Validate an Action-Token Grammar

Implement parse_action_tokens(tokens, vocabulary). tokens has shape(B,D+1). Its first column must contain only0 or1. Every remaining token must occur in vocabulary; reject unknown IDs, including reserved flags in action positions. Return (bins,termination), shapes(B,D) and(B,), by applying the inverse vocabulary map and copying the first column.

Array inputs must be NumPy int64, not lists, bool arrays, floating arrays or int32. All output arrays use int64 and fresh independent storage; preserve inputs and support noncontiguous arrays. B may be zero and is at most1024; D is in[1,64]. The supplied vocabulary has shape(K,),2<=K<=4096, contains unique integer token IDs in[2,1_000_000], and explicitly excludes the reserved termination IDs0 and1.

The format is an original teaching grammar inspired by RT-2's action-token interface, not the exact pretrained tokenizer of either RT-2 model. Each row is [termination,channel0,...,channelD-1]. Termination0 means continue and1 means terminate; D action fields are required in either case. Values are already quantized bins: no physical quantization, detokenization to actuator units, text parsing, special BOS/EOS tokens or actual execution occurs. Channel order, frame, control period and normalization are fixed by the upstream action codec.

Raise TypeError for a non-array argument. Raise ValueError for every dtype/shape/value/vocabulary/grammar violation. Reject the whole batch if any row is invalid; do not return partial successes.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2307.15818), Section3.2: action tokenization and valid output format. This is a bounded original component, not the paper's complete model.
