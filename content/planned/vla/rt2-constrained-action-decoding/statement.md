# Constrain Autoregressive Decoding to Valid Actions

Implement constrained_action_step(logits, vocabulary, positions, channels), returning (tokens, probabilities).

logits is a finite NumPy float64 array (B,V), with 0 <= B <= 256, 4 <= V <= 65536, at most 1,000,000 entries, and absolute values <= 100. vocabulary is a NumPy int64 array (K,), with 2 <= K <= min(4096,V-2), containing unique token IDs in [2,V). Its order may be arbitrary. positions is int64 (B,). channels is a built-in int excluding bool, in [1,64], and each position is in [0,channels]. Noncontiguous arrays are valid.

This follows the existing original fixed-width action grammar: position 0 is a termination flag with allowed IDs {0,1}; positions 1 through channels are action fields with allowed IDs from vocabulary. A termination flag of 1 does not remove the remaining fields. The current position is supplied, not inferred from an input sequence. No other token is allowed at that position.

For each row, softmax only its allowed logits, with all forbidden probabilities exactly zero. Return probabilities as a new float64 array (B,V), and tokens as a new int64 array (B,) selecting the allowed maximum logit. If allowed logits tie, choose the smallest numeric token ID, independently of vocabulary ordering. No sampling, temperature parameter, beam search, language-model call or full-sequence generation is included. Empty B returns the corresponding empty arrays.

Preserve inputs, use independent storage for both outputs, and validate the entire batch before returning. Non-array logits/vocabulary/positions raises TypeError; all other violations, including invalid channels, raise ValueError. Scores, probabilities, IDs and field positions are dimensionless. Physical action bounds, channel order, frame and control period belong to the upstream codec. This teaching grammar is not an exact RT-2 tokenizer, and grammar-valid output does not establish robot safety.

## Worked examples

## Flag and action rows share one logit width

Let vocabulary=[4,2], positions=[0,1], channels=2, all integer arrays int64. For float64 logits

~~~python
[[0, log(3), 50, 50, 50],
 [99, 99, 0, 99, log(3)]]
~~~

return tokens=[1,4] and probabilities=[[0.25,0.75,0,0,0],[0,0,0.25,0,0.75]]. Large forbidden logits never enter either normalizer.

## A tie follows token identity

With logits=[[0,0,0,0,0]], vocabulary=[4,2], positions=[2] and channels=2, return tokens=[2] and probabilities=[[0,0,0.5,0,0.5]]. Choosing the first vocabulary entry would incorrectly return 4.
