# Solution explanation

Union episode indices by identical scene and collector keys, keeping the two key namespaces distinct. Group by final representatives, label each group with its smallest episode ID, and move a group wholly to test when any of its scenes is held out. Union by size with path compression avoids a quadratic all-pairs graph. Work O(N alpha(N)+N log N), storage O(N).
