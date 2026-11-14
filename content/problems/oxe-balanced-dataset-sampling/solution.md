## Approach

Validate the finite probability mass, construct the ordered CDF, search with side=right, then scale each local uniform by its selected dataset size.

O(G+N log G) time and O(G+N) storage.
