# Solution explanation

Validate observed labels, map sorted dataset identities to output rows, and accumulate observed true/predicted class pairs. Divide diagonal counts by row support, then average only supported recalls. Work O(N+MK squared), storage O(N+MK squared).
