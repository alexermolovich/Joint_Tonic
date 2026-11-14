# Solution explanation

Group by source video, sort intervals, and sweep using start minus the component maximum end. Emit each completed component with its lexical-smallest clip ID and propagated split. Work O(N log N), storage O(N); no quadratic graph is built.
