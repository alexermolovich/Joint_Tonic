# Worked code examples

The schema is explicit input. A validator reports anomalies; it never repairs observations or converts their physical units.

## Example 1: a valid episode

```python
from solution import validate_episodes

schema = {'signals': {'joints': {
    'shape': [2], 'dtype': 'float', 'unit': 'rad',
    'frame': 'robot', 'min': -3., 'max': 3.
}}}
episodes = [{'timestamps': [0.,0.1], 'signals': {'joints': {
    'values': [[0.,1.], [1.,2.]], 'unit': 'rad', 'frame': 'robot'
}}}]
print(validate_episodes(episodes, schema))
```

Expected output:

```text
[]
```

Every signal row aligns with one timestamp and satisfies the shape, numeric, physical-metadata, and range contracts.

## Example 2: independent anomalies retain their locations

```python
from solution import validate_episodes

schema = {'signals': {'joints': {
    'shape': [2], 'dtype': 'float', 'unit': 'rad',
    'frame': 'robot', 'min': -3., 'max': 3.
}}}
episodes = [{'timestamps': [0.,0.], 'signals': {'joints': {
    'values': [[0.,1.], [4.,2.]], 'unit': 'rad', 'frame': 'robot'
}}}]
for issue in validate_episodes(episodes, schema):
    print(issue)
```

Expected output:

```text
{'episode': 0, 'path': 'signals.joints.values[1]', 'code': 'range'}
{'episode': 0, 'path': 'timestamps[1]', 'code': 'nonmonotonic'}
```

The stale timestamp does not hide the separate range violation. Lexicographic path ordering makes the report reproducible.

## Example 3: a schema error is different from bad data

```python
from solution import validate_episodes

schema = {'signals': {'joints': {'shape': [0], 'dtype': 'float'}}}
try:
    validate_episodes([], schema)
except ValueError as error:
    print(type(error).__name__)
```

Expected output:

```text
ValueError
```

A per-timestamp dimension must be positive. The caller must fix its schema before episode validation can proceed.
