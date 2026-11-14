# Hints

1. Validate every episode before allocating the padded tensor.

2. Compute lengths and the maximum length once.

3. Allocate zero data and false validity, then fill each episode's prefix.

