# Solution explanation

Validate strict timestamp order and every positive-duration interval, then binary-search both endpoints. Work O(T+A log T), including validation; output storage O(A).
