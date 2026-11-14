# Hints

1. Process by start then name; source-list order is not the allocation order.
2. Track the current occupant end for each persistent buffer.
3. Reuse the smallest sufficient free capacity, then smallest ID.
