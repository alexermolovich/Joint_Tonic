# Solution explanation

Validate every identity and span before computing results. Sort each request’s spans; add only the part beyond the rightmost covered endpoint. Subtract union coverage from the boundary duration and from summed span durations to distinguish missing instrumentation from overlap. Work O(N log N), storage O(N).
