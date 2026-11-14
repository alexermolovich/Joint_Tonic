# Solution explanation

Compute the original profile, then gather one replicate at a time using task indices and supplied within-task indices. Loop over thresholds or replicate curves to avoid a four-dimensional comparison allocation. Work O((B+1)MNQ), working storage O(MN+BQ).
