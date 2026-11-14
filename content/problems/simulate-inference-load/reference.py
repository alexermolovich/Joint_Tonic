def simulate_inference_load(service_ns, scenario, arrivals_ns=None):
    if type(service_ns) is not list or len(service_ns)>100000 or any(type(d) is not int or not 1<=d<=10**12 for d in service_ns):raise ValueError("service durations")
    if type(scenario) is not str or scenario not in ('single_stream','server'):raise ValueError("scenario")
    if scenario=='single_stream':
        if arrivals_ns is not None:raise ValueError("closed-loop arrivals are implicit")
    else:
        if type(arrivals_ns) is not list or len(arrivals_ns)!=len(service_ns) or any(type(a) is not int or not 0<=a<=2**63-1 for a in arrivals_ns):raise ValueError("arrival timestamps")
        if any(b<a for a,b in zip(arrivals_ns,arrivals_ns[1:])):raise ValueError("arrival order")
    previous=0;out=[]
    for i,duration in enumerate(service_ns):
        arrival=previous if scenario=='single_stream' else arrivals_ns[i]
        start=max(arrival,previous);finish=start+duration
        out.append((arrival,start,finish,finish-arrival));previous=finish
    return out
