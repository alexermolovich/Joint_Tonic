# Worked schedules and boundaries

The full input graphs are in statement.md.

- Newly ready example: initial ready IDs are decode and z-audit. After decode, ready IDs are train and z-audit. Output: ["decode", "train", "z-audit"].
- Merge example: fit has two distinct parents. After images it still has one; after labels it has zero. Output: ["images", "labels", "fit", "report"].

~~~python
schedule_pipeline([], [])  # []
schedule_pipeline(["a", "b"], [("a", "b"), ("a", "b")])  # ["a", "b"]
schedule_pipeline(["a"], [("a", "a")])  # ValueError
schedule_pipeline(["a", "b", "c"], [("b", "c"), ("c", "b")])  # ValueError
~~~

The last call must not return ["a"]. Theory question 1: a newly ready ID can sort before a previously ready ID. Question 2: ordering contains no artifact-version evidence. These fixtures are public teaching examples.
