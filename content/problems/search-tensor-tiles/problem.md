# Search Tensor Tile Sizes with a Toy Cost Model

Implement select_tensor_tile(shape, candidates, memory_bytes, launch_cost) -> tuple | None.

shape=(M,N,K), positive built-in non-bool ints <=4096, describes A(M,K)B(K,N). candidates is a list of 1–4096 unique tuples(tm,tn,tk), positive built-in ints <=256. memory_bytes is a built-in int in[1,2**31]; launch_cost is a built-in int in[0,10**9]. Each candidate uses a teaching float32 tile footprint F=4*(tm*tk+tk*tn+tm*tn) bytes. It is feasible when F<=memory_bytes; tile sizes may exceed a matrix dimension and use padding.

Let Q=ceil(M/tm)*ceil(N/tn)*ceil(K/tk). The ORIGINAL toy cost is C=Q*(tm*tn*tk+launch_cost), counting padded scalar multiply-accumulate units and tile launches. Select minimum(C,F,tm,tn,tk) lexicographically among feasible candidates. Return(tm,tn,tk,C,F), all built-in ints; return None when none fit. Validate all candidates even when an earlier one already wins. Preserve inputs. All malformed inputs raise ValueError.

These costs are dimensionless teaching scores, not measured cycles, latency, real cache use, or TVM's learned cost model. The footprint assumes one A,B,C tile with no double buffering; full matrix storage is outside this candidate model.

## Worked examples

### Launch cost changes the choice
`select_tensor_tile((3,3,3),[(1,1,1),(2,2,2)],48,10)` returns `(2,2,2,144,48)`.

### Memory excludes the larger tile
With the same shape/candidates/cost but `memory_bytes=47`, return `(1,1,1,297,12)`. With memory11, return None.

## Source and scope

This original bounded component is motivated by [2018-tvm](https://www.usenix.org/conference/osdi18/presentation/chen). It does not reproduce the full paper, trained model or benchmark protocol.
