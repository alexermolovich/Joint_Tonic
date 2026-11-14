# Worked examples

### Exact thresholds are accepted

~~~python
protocol={"scenario":"server","model_sha256":"a"*64,
          "min_queries":10,"min_duration_ns":100,"min_quality":0.8}
run={"scenario":"server","model_sha256":"a"*64,"expected_queries":10,
     "completed_queries":10,"failed_queries":0,"duration_ns":100,"quality":0.8}
benchmark_run_rejections(run,protocol)
# []
~~~

The evidence matches identity, accounting, coverage, duration and quality.

### One failed query and one unfinished query

~~~python
run={"scenario":"server","model_sha256":"a"*64,"expected_queries":10,
     "completed_queries":8,"failed_queries":1,"duration_ns":99,"quality":0.79}
protocol={"scenario":"server","model_sha256":"a"*64,
          "min_queries":9,"min_duration_ns":100,"min_quality":0.8}
benchmark_run_rejections(run,protocol)
# ["failed_queries","incomplete","insufficient_duration",
#  "insufficient_queries","quality"]
~~~

A failure and an unfinished query are different evidence. Neither is counted as successful completed work.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

