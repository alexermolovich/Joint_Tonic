def select_tensor_tile(shape, candidates, memory_bytes, launch_cost):
    def triple(x,limit):return type(x) is tuple and len(x)==3 and all(type(v) is int and 1<=v<=limit for v in x)
    if not triple(shape,4096) or type(candidates) is not list or not 1<=len(candidates)<=4096 or any(not triple(t,256) for t in candidates):raise ValueError("shape/candidates")
    if len(set(candidates))!=len(candidates):raise ValueError("duplicate candidates")
    if type(memory_bytes) is not int or not 1<=memory_bytes<=2**31 or type(launch_cost) is not int or not 0<=launch_cost<=10**9:raise ValueError("budget/cost")
    best=None;m,n,k=shape
    for tm,tn,tk in candidates:
        footprint=4*(tm*tk+tk*tn+tm*tn)
        if footprint>memory_bytes:continue
        q=((m+tm-1)//tm)*((n+tn-1)//tn)*((k+tk-1)//tk)
        candidate=(q*(tm*tn*tk+launch_cost),footprint,tm,tn,tk)
        if best is None or candidate<best:best=candidate
    return None if best is None else (best[2],best[3],best[4],best[0],best[1])
