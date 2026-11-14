# Worked cache decisions

Full inputs are in statement.md.

1. Changed raw reaches raw → features → model → report. The cache contains model, report, lookup. Intersection: ["model", "report"].
2. Changed model reaches model → report. Raw is a parent, not a consumer. Intersection: ["model", "report"].

~~~python
invalidated_artifacts({}, [], [])  # []
invalidated_artifacts({"raw": []}, [], ["raw"])  # []
invalidated_artifacts({"raw": []}, ["raw"], ["raw"])  # ["raw"]
invalidated_artifacts({"a": ["b"], "b": ["a"]}, [], [])  # ValueError
~~~

Question 1: model changing does not imply its input data changed. Question 2: paths/names do not establish dependency versions or content identity. These are original public examples.
