## Approach

For each candidate L, partition the residual array into consecutive chunks, cumulatively sum each along time, accumulate squared entries, and divide by T*D.

O(K*T*D) time; O(T*D+K) working space.
