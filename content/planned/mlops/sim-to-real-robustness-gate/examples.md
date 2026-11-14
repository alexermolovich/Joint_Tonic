# Worked examples

### Exact thresholds pass
required["a"], expected_distribution="a"*64, thresholds min_trials10,min_success_rate0.8,min_worst_return=-1, evidence[{slice:"a",distribution_sha256:"a"*64,trials:10,successes:8,worst_return:-1}] returns approvedTrue,reasons[].

### All independent failures are visible
required["b","a"], same thresholds, evidence[{slice:"a",distribution_sha256:"b"*64,trials:5,successes:1,worst_return:-2}] returns approvedFalse,reasons["a:distribution","a:trials","a:success","a:worst-return","b:missing"].
