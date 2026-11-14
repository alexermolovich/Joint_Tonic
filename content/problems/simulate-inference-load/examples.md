# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

