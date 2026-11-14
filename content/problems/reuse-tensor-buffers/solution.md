# Solution explanation

Sort tensor allocations by start and name. A min-heap releases buffers at their half-open lifetime end; an ordered free list selects the smallest fitting capacity and then buffer ID. Existing capacity never shrinks or grows. Sum all created capacities, not merely live allocations. Sorting and heap work O(N log N); Python list insertions/removals can make worst-case O(N²), bounded at 10,000 records.
