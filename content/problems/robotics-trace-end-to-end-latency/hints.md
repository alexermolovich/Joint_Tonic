# Hints

1. Index events by request ID and boundary, rejecting duplicates.

2. Validate one shared clock and complete pairs before returning results.

3. Subtract Python integers and sort request IDs, not event timestamps.

