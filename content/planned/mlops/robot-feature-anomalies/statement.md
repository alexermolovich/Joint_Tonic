# Detect Missing, Range, Domain, and Shape Anomalies

Implement feature_anomalies(records, schema) -> list[tuple[int,str,str]].

schema is a dictionary of 1–128 feature names. records is a Python list of 0–1,000 dictionaries, each containing at most128 feature names. Names match ASCII [a-z][a-z0-9_-]{0,63}. An invalid outer container/name is ValueError.

Each schema entry has exactly kind, shape, required, minimum, maximum, domain:
- kind is the string numeric or categorical.
- shape is a tuple of 0–4 built-in positive integer dimensions, each<=128 and product<=1024; () means a scalar.
- required is a built-in bool.
- For numeric, minimum/maximum are built-in non-bool int/float, finite with abs<=1e6 and minimum<=maximum; domain must be None.
- For categorical, minimum and maximum must be None; domain is a nonempty tuple of at most128 unique ASCII labels matching the same name rule.

Record values may be malformed data; report one issue per feature using the priority below. If a record value is any NumPy array, its size must be<=1024 and total elements across all record arrays must be<=1,000,000; exceeding those workload bounds raises ValueError before anomaly detection. Other value types have no recursive interpretation.

For each record, emit (record_index,feature_name,code):
- A supplied name absent from schema: unexpected.
- Absent required field: missing. Absent optional field: no issue.
- Present field not a NumPy array: type.
- Array shape differs from schema: shape.
- Numeric array dtype is not float64, or categorical dtype.kind is not U (Unicode): dtype.
- Numeric array contains NaN or infinity: nonfinite.
- Finite numeric value outside inclusive [minimum,maximum]: range.
- Any categorical array entry outside domain: domain.
- Otherwise no issue.

Check in that order and emit at most one code per record/feature. A shape error suppresses dtype/range/domain checks. Unexpected fields are not checked against a fabricated schema. Sort by (record_index,feature_name,code); indices are built-in ints. Empty records returns []. Preserve all inputs. Malformed schema fields raise ValueError; malformed feature values normally produce issue records as specified.

## Worked examples

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

## Source and scope

The source motivates schema validation and located anomalies. This small numeric/categorical schema is original and complements the existing full episode validator; it does not infer a schema, convert physical units or implement every production validation rule. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).
