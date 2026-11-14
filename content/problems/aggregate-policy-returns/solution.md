# Solution explanation

Sort each policy’s episodes. Include floor(alpha E) returns and a fractional boundary return. When that count is zero, return the minimum directly to avoid subnormal multiplication underflow. Full-tail mode avoids an out-of-range boundary index. Work O(P E log E), storage O(P E).
