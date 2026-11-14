# Solution

Validate the complete padded target set and every supplied assignment. Reject references to invalid slots and duplicate use of a target in the same image. Initialize query classes to C and weights to eos_weight, then fill matched entries from the target labels with unit weight. The assignment itself is an input; no matching solver or loss reduction is hidden here. Time is O(B(M+Q log Q)) with per-row duplicate validation.
