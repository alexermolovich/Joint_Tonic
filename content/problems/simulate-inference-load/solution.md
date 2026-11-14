# Solution explanation

Maintain the previous finish time as a built-in integer. In single-stream mode that completion becomes the next arrival. In server mode use the supplied arrival; start at the greater of it and the previous finish. Add service, subtract arrival, and append the exact tuple. Never convert timestamps to float or int64. Work/output storage are O(N).
