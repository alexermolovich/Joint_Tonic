# Score a Robot ML System for Production Readiness

Implement:

~~~python
def readiness_score(checks: dict[str, list[str]]) -> dict:
    ...
~~~

Require exactly these dictionary keys: data, model, infrastructure, monitoring. Each value is a Python list of 0–7 status strings, one per distinct check chosen upstream. Allowed statuses are none, manual, automated. Their credits are 0.0, 0.5, 1.0 respectively. manual means a completed, documented, distributed manual check; automated means a repeated automatic test exists. These statuses describe evidence practice, not whether a model currently passes the check.

Return exactly {"categories": {category: sum_of_credits, ...}, "score": minimum_category_sum}. Category keys use the four names above; every numeric output must be a Python float. Dict insertion order is not graded. Empty category lists sum to 0.0, and four empty lists return score0.0. Repeated status strings are allowed because different checks may share a status. Never average, normalize by check count, drop an empty category, or count a check twice.

Malformed dictionary/list/status types, missing/extra keys, or more than seven items in a category raise ValueError. No mutation. Inputs are ordinary CPU Python metadata; there are no frames, units of motion, tensors, clocks or sampling.

## Worked examples

### The least-covered category controls the score

~~~python
checks = {"data":["automated","manual"], "model":["automated"],
          "infrastructure":["manual","none"], "monitoring":["automated","automated"]}
readiness_score(checks)
# {"categories":{"data":1.5,"model":1.0,"infrastructure":0.5,"monitoring":2.0},
#  "score":0.5}
~~~

Infrastructure limits the result even though other categories have more evidence.

### Empty evidence is visible

~~~python
checks = {"data":[], "model":[], "infrastructure":[], "monitoring":[]}
readiness_score(checks)
# {"categories":{"data":0.0,"model":0.0,"infrastructure":0.0,"monitoring":0.0},
#  "score":0.0}
~~~

Missing coverage is represented by zero credit, not by omitting the category.

## Source and scope

The half-point/manual, full-point/automated and minimum-category aggregation follows the paper. Supplied check lists and robot examples are original; this function does not reproduce the paper's full28-check questionnaire or certify operational safety. [Primary source](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
