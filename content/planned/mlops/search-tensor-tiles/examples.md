# Worked examples

### Launch cost changes the choice
`select_tensor_tile((3,3,3),[(1,1,1),(2,2,2)],48,10)` returns `(2,2,2,144,48)`.

### Memory excludes the larger tile
With the same shape/candidates/cost but `memory_bytes=47`, return `(1,1,1,297,12)`. With memory11, return None.
