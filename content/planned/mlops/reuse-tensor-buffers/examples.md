# Worked examples

### Reuse and concurrent allocation
`reuse_tensor_buffers([("a",8,0,2),("b",4,2,3),("c",8,2,4)])` returns `{"assignments":[("a",0),("b",0),("c",1)],"capacities":[8,8],"reserved_bytes":16}`.

### Best-fit chooses the smaller sufficient buffer
For `[("a",8,0,1),("b",4,0,1),("c",3,1,2)]`, return assignments `[("a",0),("b",1),("c",1)]`, capacities `[8,4]`, reserved_bytes12.
