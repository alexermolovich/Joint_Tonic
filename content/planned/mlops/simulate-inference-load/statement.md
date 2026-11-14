# Simulate Single-Stream and Server Load

Implement simulate_inference_load(service_ns, scenario, arrivals_ns=None) -> list[tuple[int,int,int,int]].

service_ns is a Python list of0–100,000 built-in non-bool ints, each in[1,10**12], representing fixed service durations. scenario is the string single_stream or server.
- single_stream requires arrivals_ns is None. Request0 arrives at0; every later request arrives exactly when the previous one completes.
- server requires arrivals_ns is a Python list of the same length, with built-in non-bool ints in[0,2**63-1], nondecreasing. Equal arrivals retain input request order.

One server processes requests in input order without overlap, preemption or batching. For request i, start=max(arrival,previous_finish), finish=start+service_ns[i], latency=finish-arrival. Use previous_finish=0 before the first request. Return one tuple(arrival,start,finish,latency) per request in input order; all fields are built-in ints. No output timestamp is truncated to int64: valid accumulated finish times may exceed2**63-1.

Empty services returns[] with None arrivals in single_stream or[] arrivals in server. Preserve inputs. All malformed types, bounds, order, unsupported scenarios or mismatched arrivals raise ValueError. No exponential RNG arrivals are generated; supplied server arrivals may be any valid deterministic trace. Latency includes queue waiting and service time, but no unmodeled network or preprocessing time.

## Worked examples

### Closed-loop single-stream requests

~~~python
simulate_inference_load([3,2,4],"single_stream")
# [(0,0,3,3),(3,3,5,2),(5,5,9,4)]
~~~

Each new request is issued only after completion of the previous one, so this synthetic scenario has no queue wait.

### Server arrivals create a queue

~~~python
simulate_inference_load([3,2,4],"server",[0,1,8])
# [(0,0,3,3),(1,3,5,4),(8,8,12,4)]
~~~

Request1 waits2ns, then runs2ns; its latency is4ns. Request2 arrives after the server is idle and starts immediately.

## Source and scope

The historical MLPerf2019 paper motivates scenario-dependent query issuance. The supplied-arrival, single-server FCFS recurrence is an original teaching simulator, not the official LoadGen or compliance protocol. [Primary source](https://arxiv.org/html/1911.02549v1).

