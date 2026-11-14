# Worked examples

put object a(hash"1"*64, size=4) on n1, repeat same put, then put on n2 produces nodes["n1","n2"], lost=False, physical_bytes=8.

put a(size=4) on n1, evict a/n1 twice produces nodes[], lost=True, physical_bytes=0, while retaining a's immutable hash and size. A later put with a different hash is invalid.
