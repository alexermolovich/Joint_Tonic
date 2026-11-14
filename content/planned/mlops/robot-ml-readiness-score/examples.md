# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
