# Solution explanation

Validate the entire interface, including the vocabulary for empty batches. Allocate zero probabilities so every forbidden token stays exactly zero. Sort a private copy of the action IDs; `argmax` then resolves equal scores by the smallest numeric ID, rather than caller vocabulary order.

For each row, choose flag IDs `[0,1]` at position zero or the action IDs at later positions. Subtract the largest *allowed* logit, exponentiate, and divide by the sum over that same allowed set. Write only those probabilities and return the allowed maximizing token.

A full-vocabulary softmax followed by masking fails because the forbidden logits still contribute to the denominator. Choosing a maximum before masking can emit an ordinary language token instead of an action field.

With batch size $B$, vocabulary width $V$, and $K$ allowed action IDs, validation and zeroing cost $O(BV)$, sorting costs $O(K\log K)$, and normalization costs $O(BK)$. Output storage is $O(BV+B)$, with $O(K)$ temporary working storage. The grammar checks token syntax; collision checks and physical action interpretation remain outside this component.
