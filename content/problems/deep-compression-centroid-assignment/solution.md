# Solution explanation

Build the absolute distance matrix between each weight and each supplied centroid. Argmin along the original centroid axis gives the required first-index tie. Select index-1 and reconstructed0 for inactive weights, including when their nearest centroid is nonzero. Empty N returns typed empty arrays. Work and straightforward distance storage O(NK); no centroid fitting occurs.
