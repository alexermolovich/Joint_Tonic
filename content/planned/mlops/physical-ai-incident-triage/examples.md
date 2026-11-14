# Worked examples

### Strongest event sets the component priority

~~~python
events = [(900,"arm","model_error"),(950,"arm","safety_stop"),
          (920,"camera","sensor_stale"),(800,"camera","model_error"),
          (980,"planner","deadline_miss")]
triage_events(events,1000,150)
# [("arm","P0",2,900),("camera","P1",1,920),("planner","P1",1,980)]
~~~

The cutoff is850ms. Camera's800ms event is excluded. Arm's earliest retained event is900ms even though the strongest event occurred later.

### Inclusive cutoff and duplicate records

~~~python
events = [(90,"b","model_error"),(100,"a","model_error"),
          (90,"b","model_error"),(89,"a","safety_stop")]
triage_events(events,100,10)
# [("b","P2",2,90),("a","P2",1,100)]
~~~

Both90ms records count. The stale P0 record does not raise the retained priority of a.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
