# Estimate Memory, Latency, and Quantized Serving Budgets

Four-bit weights occupy fewer bytes, but packed storage and kernel speed are separate questions. Combine exact weight-byte arithmetic with measured latency and explicitly supplied runtime overhead to decide whether a configuration fits both limits.

## Contract

parameter_count built-in integer1..10^12; bits integer vector(C,) values4,8,16,32,1<=C<=128; overhead_bytes and kv_bytes integer(C,), each0..1e6; latency_ms real(C,K),1<=K<=4096, strictly positive. memory_limit built-in integer0..10^13; deadline_ms realpositive<=1e6. Packed weight bytes=ceil(parameter_count*bits/8), no assumed speedup from quantization. Add supplied overhead and KV cache. p95 latency nearest rank ceil(.95*K)-1. Return weight_bytes/total_bytes int64(C,), p95_latency_ms float64(C,), feasible bool(C,) requiring total<=limit AND p95<=deadline. This excludes unspecified activations and training optimizer memory; supply overhead appropriate for this teaching budget.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Memory bytes; latency/deadline milliseconds; parameter and token counts dimensionless. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.


## Example 1

N=3,bits=[4,8],overhead=[3,3],KV=[4,4],latencies=[[2,3],[2,4]],memory_limit9,deadline3 gives weights[2,3],total[9,10],p95[3,4],feasible[True,False].

## Example 2

N=2,bits=[4],overhead=[0],KV=[0],latency[[5]],memory_limit1,deadline5 is feasible: both boundary equalities pass.
