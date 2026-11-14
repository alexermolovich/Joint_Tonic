# Solution explanation

First validate topology and count every consumer. Then traverse topologically: extend the parent group only across compatible pointwise operators whose parent has exactly one consumer. Otherwise start a group. Full-graph counts prevent fusing across a branch discovered later. Work and storage O(N).
