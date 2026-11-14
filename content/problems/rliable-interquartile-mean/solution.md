# Solution explanation

Promote to float64, validate the complete matrix, sort its flattened entries and average the interval [k,K-k). Sorting dominates: O(K log K) work and O(K) storage. Trimming rows separately would answer a different question.
