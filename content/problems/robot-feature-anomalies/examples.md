# Worked examples

### Missing versus out of range

~~~python
schema = {"joint":{"kind":"numeric","shape":(2,),"required":True,
                   "minimum":-1.0,"maximum":1.0,"domain":None}}
records = [{"joint":np.array([0.,2.])}, {}]
feature_anomalies(records,schema)
# [(0,"joint","range"),(1,"joint","missing")]
~~~

A missing measurement is not a zero vector.

### Shape has priority over categorical content

~~~python
schema = {"terrain":{"kind":"categorical","shape":(),"required":False,
                     "minimum":None,"maximum":None,"domain":("dry","wet")}}
records = [{"terrain":np.array("snow")},
           {"terrain":np.array(["snow"])}, {"extra":None}, {}]
feature_anomalies(records,schema)
# [(0,"terrain","domain"),(1,"terrain","shape"),(2,"extra","unexpected")]
~~~

The second value is a length-one vector rather than a scalar, so its content is not checked. The absent optional field is allowed.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
