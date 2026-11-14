# Solution

Form query-by-training cosine scores, stable-sort neighbors, and retain the first k. Apply a stable softmax only within each selected neighborhood, then accumulate weights by training label. Argmax selects the lowest class index on exact ties. Empty query batches retain the class dimension. Feature extraction, split design and accuracy computation remain outside this function. Similarity costs O(NMD), neighbor sorting O(NM log M).
