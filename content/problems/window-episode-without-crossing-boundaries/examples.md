## Worked examples

1. `episode_ids=[4,4,4,8,8], window=2, stride=1` → `[[0,1],[1,2],[3,4]]`.
2. `episode_ids=[1,1,1,1,2], window=3, stride=2` → `[[0,1,2]]`; no partial window is returned.
