# Worked examples

### Uneven completions
`graph_throughput_jitter({"vision":[0,10,30,40]}, (0,40))` returns `{"vision":{"count":3,"throughput_hz":75000000.0,"mean_interval_ns":15.0,"jitter_ns":5.0}}`.

### One retained event
`graph_throughput_jitter({"control":[5,15]}, (0,10))` returns `{"control":{"count":1,"throughput_hz":100000000.0,"mean_interval_ns":None,"jitter_ns":None}}`.
