# Evaluate Frozen Features with k-NN

Implement knn_classify(train, labels, queries, k, num_classes, temperature). train and queries are finite NumPy float64, shapes (M,D),(N,D), 1<=M<=512,0<=N<=512,1<=D<=256. Every feature row has L2 norm1 within atol1e-6,rtol0. labels is NumPy int64 (M,), in [0,num_classes). k and num_classes are built-in ints excluding bool;1<=k<=M,1<=num_classes<=1000. temperature is built-in int/float excluding bool in [1e-4,1e4]. Compute cosine dot products, choose k largest similarities per query with lower training index breaking ties, apply stable softmax over selected similarities divided by temperature, and sum normalized neighbor weights by class. Return new int64 predictions(N,) using lowest class index on tied class scores, and float64 scores(N,num_classes). Empty queries allowed; inputs unchanged, noncontiguous supported. TypeError for any non-array among first3; ValueError for all other violations. Features are dimensionless frozen representations; no fitting, self-exclusion, row normalization, or accuracy calculation. A query may also be in train; it is not silently removed. Normalizing votes is a teaching convention that preserves the usual weighted-kNN ranking.

## Worked examples

## Closest prototype

train=[[1,0],[0,1],[-1,0]], labels=[0,1,1], queries=[[1,0],[0,1]], k=1,num_classes=2,temperature=1. Return predictions=[0,1], scores=[[1,0],[0,1]].

## Weighted vote

train=[[1,0],[0,1]], labels=[0,1], queries=[[1,0]], k=2,num_classes=2,temperature=1. Selected similarities[1,0] give scores=[[.7310585786,.2689414214]], prediction=[0].

## Hints

1. Stable-sort cosine similarities per query.
2. Subtract the selected maximum before exponentiation.
3. Accumulate neighbor weights into class columns; use argmax for lowest-index ties.
