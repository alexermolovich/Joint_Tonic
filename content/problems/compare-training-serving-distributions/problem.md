# Compare Training and Serving Distributions

Implement:

~~~python
def categorical_skew(train_counts: dict[str, int],
                     serve_counts: dict[str, int],
                     threshold: float) -> dict:
    ...
~~~

Each dictionary has at most10,000 category keys matching ASCII [a-z][a-z0-9_-]{0,63}. Counts are built-in non-bool integers in [0,10**12]. Each histogram must have a strictly positive total; empty or all-zero histograms raise ValueError because their probabilities are undefined. Zero-count categories are otherwise allowed.

threshold is a built-in non-bool int/float, finite and in [0,1]. Align over the sorted union of category names, supplying zero count for a name absent from either dictionary. Let p and q be each histogram's own normalized frequencies. Return exactly:
- deltas: a Python list of (category, float(q-p)) tuples in ASCII name order, including zero differences.
- distance: Python float max(abs(q-p)) over the union.
- flagged: Python bool distance > threshold. Equality is accepted.

Compute normalized frequencies in Python float64 semantics. Numerical outputs use rtol=1e-12,atol=1e-12; flagged, order and structure are exact and are evaluated on inputs away from ambiguous rounding except exactly representable boundaries. Preserve inputs. No smoothing pseudocounts, sample-size weighting, data collection, clock inference or RNG. Every malformed key, count, threshold or exceeded bound raises ValueError.

## Worked examples

### More samples do not necessarily mean drift

~~~python
categorical_skew({"indoor":2,"outdoor":2},
                 {"indoor":20,"outdoor":20},0)
# {"deltas":[("indoor",0.0),("outdoor",0.0)],"distance":0.0,"flagged":False}
~~~

Both distributions are50% indoor and50% outdoor despite different totals.

### Align a new operating category

~~~python
categorical_skew({"dry":3,"wet":1},{"dry":1,"snow":1},0.25)
# {"deltas":[("dry",-0.25),("snow",0.5),("wet",-0.25)],
#  "distance":0.5,"flagged":True}
~~~

Train has no snow observations, so its snow probability is zero. The largest change is0.5.

## Source and scope

The paper motivates comparisons of dataset statistics. This aligned maximum-frequency-difference contract is an explicit teaching metric; its threshold is supplied and is not a statistical significance test or complete drift detector. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).
