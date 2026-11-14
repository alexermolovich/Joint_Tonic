# Solution explanation

Maintain each artifact's original digest/size and a set of nodes. Validate every later put against that identity, including after the set becomes empty. Apply put as set addition and evict as discard, then sum size times replica count using Python integers. Work O(E) plus sorting artifacts and node lists; storage O(A+replica pairs).
