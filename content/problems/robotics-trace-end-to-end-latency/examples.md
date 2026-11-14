# Worked examples

### Correlation beats event-list order

~~~python
trace_latencies([("b","output",150,"mono"),("a","input",100,"mono"),
                 ("b","input",110,"mono"),("a","output",160,"mono")])
# [("a",60),("b",40)]
~~~

The earlier output belongs to b, not the earliest input a. Nearest-time matching would change the measurements.

### Preserve small differences at large clock values

~~~python
trace_latencies([("tiny","input",2**63-3,"mono"),
                 ("tiny","output",2**63-1,"mono"),
                 ("same","input",8,"mono"),("same","output",8,"mono")])
# [("same",0),("tiny",2)]
~~~

Integer arithmetic keeps the2ns difference; converting large timestamps to floats could erase it.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

