# Worked code examples

These examples inspect selected fields from the full decision object. All latency units are milliseconds; throughput is queries per second for sequential measurements.

## Example 1: complete evidence passes

```python
from solution import release_gate

samples = [
    {'hardware':'cpu', 'latency_ms':10., 'memory_mb':100., 'correct':True},
    {'hardware':'cpu', 'latency_ms':20., 'memory_mb':120., 'correct':True},
]
policy = {'min_samples':2, 'min_accuracy':0.9, 'max_p99_ms':20.,
          'min_throughput_qps':60., 'max_memory_mb':128.}
result = release_gate(samples, policy)
metrics = result['metrics']['cpu']
print(result['passed'], result['reasons'])
print([metrics[k] for k in ('p50_ms','p90_ms','p99_ms')])
print(f"{metrics['throughput_qps']:.6f}")
```

Expected output:

```text
True []
[15.0, 19.0, 19.9]
66.666667
```

The linear p99 estimate is 19.9 ms. Sequential throughput is `2000/30`, not the mean of `1000/10` and `1000/20`.

## Example 2: a tail-latency failure retains the evidence

```python
from solution import release_gate

samples = [
    {'hardware':'cpu', 'latency_ms':10., 'memory_mb':100., 'correct':True},
    {'hardware':'cpu', 'latency_ms':20., 'memory_mb':120., 'correct':True},
]
policy = {'min_samples':2, 'min_accuracy':0.9, 'max_p99_ms':19.,
          'min_throughput_qps':60., 'max_memory_mb':128.}
result = release_gate(samples, policy)
print(result['passed'], result['reasons'])
print(result['metrics']['cpu']['accuracy'])
```

Expected output:

```text
False ['cpu:p99_ms']
1.0
```

Perfect accuracy does not override a missed performance rule. Metrics remain available to explain the rejection.

## Example 3: excluded warmup does not count as evidence

```python
from solution import release_gate

policy = {'min_samples':2, 'min_accuracy':0.9, 'max_p99_ms':20.,
          'min_throughput_qps':60., 'max_memory_mb':128.}
print(release_gate([{'warmup':True}], policy))
```

Expected output:

```text
{'passed': False, 'metrics': {}, 'reasons': ['no_samples']}
```

The excluded record need not contain timing fields, but an empty measurement set cannot pass the release policy.
