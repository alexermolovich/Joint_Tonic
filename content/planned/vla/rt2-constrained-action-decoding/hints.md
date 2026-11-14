# Hints

1. Construct allowed IDs from each row’s field position before taking a maximum.
2. Normalize only allowed logits; fill forbidden output probabilities with exact zeros.
3. Break maximum-logit ties by numeric token ID, not vocabulary order.
