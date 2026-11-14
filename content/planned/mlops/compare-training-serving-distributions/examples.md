# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
