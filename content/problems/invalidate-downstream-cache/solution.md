# Solution: separate reachability from cache membership

Validate every artifact and parent reference, then build outgoing consumer lists by reversing the input parent lookup. Deduplicate parent edges. A full-graph indegree traversal rejects cycles even when there are no changes or no cache entries.

Next traverse outgoing consumers from all changed artifacts. Include the roots and keep uncached nodes in the traversal: they can connect a changed source to a cached descendant. Intersect the complete reached set with cached IDs and sort.

This is a conservative recomputation plan. It does not delete files, compare hashes, or prove that an artifact's numerical content differs. Time is O(V+E+V log V) with final sorting, and memory is O(V+E).
