# Compute a Compressed Model Storage Budget

## Goal and contract

Implement `compressed_storage_budget(dense_count, frequencies, code_lengths, index_bits, centroid_bits, header_bytes) -> dict`. dense_count int1..10^12; frequencies int64(K,) counts0..10^12 with sum<=dense_count; code_lengths int64(K,) in1..32;1<=K<=256; index_bits int1..64; centroid_bits int16 or32; header_bytes int0..10^6. Validate prefix-code feasibility sum(2**(-length))<=1 exactly (multiply by2**32 and use Python integers). The caller supplies code lengths; do not construct Huffman codes. For n=sum(frequencies), symbol_bits=sum(freq*length); symbol_bytes=ceil(symbol_bits/8), index_bytes=ceil(n*index_bits/8), codebook_bytes=K*centroid_bits/8. Round the symbol and index streams separately. Return Python ints symbol_bits,symbol_bytes,index_bytes,codebook_bytes,total_bytes and dense_bytes=4*dense_count, plus float compression_ratio=dense_bytes/total_bytes. total includes header_bytes. Models use dense float32 baseline; no tensor allocator, alignment beyond bytes, or speed estimate. Work O(K).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

dense_count=10, frequencies=[3,2], lengths=[1,1], index_bits=3, centroid_bits=32, header_bytes=2 yields symbol_bits5,symbol_bytes1,index_bytes2,codebook_bytes8,total_bytes13,dense_bytes40,compression_ratio40/13.

 dense_count=1, frequencies=[0], lengths=[1], index_bits=1, centroid_bits=16, header_bytes=0 yields symbol_bits0,symbol_bytes0,index_bytes0,codebook_bytes2,total_bytes2,dense_bytes4,compression_ratio2.

## Source and scope

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
