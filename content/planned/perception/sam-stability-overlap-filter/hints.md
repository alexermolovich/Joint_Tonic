# Hints

1. Count high and low pixels over both spatial axes, without treating logits as probabilities.
2. Empty base masks fail independently of the stability threshold.
3. Sort by (-quality, original_index), then compare each candidate only to the kept list.

