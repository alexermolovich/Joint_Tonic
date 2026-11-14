# Solution explanation

Validate both complete snapshots first. Compare dataset key sets, then shared feature key sets. For shared features compare all four descriptor fields and retain every difference. Emit one dataset-level issue for wholly missing/unexpected datasets, avoiding redundant feature expansion. Finally sort the tuples. Work is O(F+K log K), where F is descriptor count and K emitted changes; output storage is O(K).
