# Reuse Tensor Buffers with Liveness Analysis

Implement reuse_tensor_buffers(tensors) -> dict.

tensors is a list of 0–10000 tuples(name,size_bytes,start,end). Names are unique ASCII IDs matching[a-z][a-z0-9_-]{0,63}. Size is built-in non-bool int in[1,10**9]; start/end are built-in ints in[0,10**9] with start<end. A tensor is live during half-open logical execution steps[start,end); these are ordering indices, not timestamps or wall latency.

Process tensors sorted by(start,name). A buffer becomes reusable when its previous occupant's end<=current start. From FREE buffers with capacity>=size, choose minimum(capacity,buffer_id). If none fit, allocate the next consecutive integer ID starting0 with capacity=size. Buffer capacities never grow or shrink. Return exactly assignments (list of(name,buffer_id) in processing order), capacities (list by buffer ID), reserved_bytes(sum of capacities). Buffers retain memory when free, so reserved_bytes is this allocator's total reserved memory, not the theoretical minimum live-byte peak. Empty input returns empty lists and0. Preserve inputs; malformed contracts raise ValueError.

No byte contents are copied, no in-place operation is inferred, and two simultaneously live tensors cannot alias. This is a deterministic best-fit interval allocator, not a globally optimal memory planner.

## Worked examples

### Reuse and concurrent allocation
`reuse_tensor_buffers([("a",8,0,2),("b",4,2,3),("c",8,2,4)])` returns `{"assignments":[("a",0),("b",0),("c",1)],"capacities":[8,8],"reserved_bytes":16}`.

### Best-fit chooses the smaller sufficient buffer
For `[("a",8,0,1),("b",4,0,1),("c",3,1,2)]`, return assignments `[("a",0),("b",1),("c",1)]`, capacities `[8,4]`, reserved_bytes12.

## Source and scope

This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.
