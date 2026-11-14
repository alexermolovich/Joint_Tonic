# Solution

Stable-sort descending raw quality scores and retain the first k original indices. Index masks and scores with the same indices and return independent arrays. No clipping, suppression, averaging, or mask conversion is performed. Sorting costs O(N log N), and copying selected masks costs O(kHW). Original indices preserve alignment with metadata outside this function.
