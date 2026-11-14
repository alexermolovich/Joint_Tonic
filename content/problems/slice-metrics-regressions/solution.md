# Solution explanation

Compute candidate-minus-baseline for every aligned episode, then aggregate counts and sums by slice. Keep unobserved means NaN and report incomplete coverage. Compare strictly above tolerance; compute pooled change from episodes rather than slice means. Work O(N+S), storage O(N+S).
