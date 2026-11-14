# Hints

1. Compute and cache one bucket per distinct scene.

2. Hash the exact canonical bytes and interpret the first eight bytes in big-endian order.

3. Walk the original episode/scene pairs once and append to one fresh output list.

