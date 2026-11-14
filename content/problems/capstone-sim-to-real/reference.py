import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Invalid scalar")
    return float(x)

import hashlib,json

def sim_to_real(success, observed, latency, seed, min_rate, max_gap, budget_ms):
    success=_array(success,2,"b");observed=_array(observed,2,"b");latency=_array(latency,2)
    N=success.shape[0]
    if not 4<=N<=1024 or success.shape!=(N,4) or observed.shape!=(N,4) or latency.shape!=(N,4):raise ValueError("shapes")
    if np.any((latency<0)|(latency>10000)) or type(seed) is not int or not 0<=seed<=2**32-1:raise ValueError("latency/seed")
    minimum=_scalar(min_rate,0,1);gap_limit=_scalar(max_gap,0,1);budget=_scalar(budget_ms,0,10000)
    strata=np.arange(N,dtype=np.int64)%4;u=np.random.Generator(np.random.PCG64(seed)).random((N,2));factors=np.column_stack((.4+.4*(strata//2+u[:,0]),.5+.5*(strata%2+u[:,1])))
    counts=np.zeros((4,4),np.int64);rates=np.full((4,4),np.nan);means=np.full(4,np.nan);worst=np.full(4,np.nan);p95=np.full(4,np.nan);wilson=np.full((4,2),np.nan);z=1.959963984540054
    for bucket in range(4):
        for domain in range(4):
            mask=(strata==bucket)&observed[:,domain];counts[bucket,domain]=mask.sum()
            if mask.any():rates[bucket,domain]=success[mask,domain].mean()
    for domain in range(4):
        mask=observed[:,domain];n=int(mask.sum())
        if n:
            rate=float(success[mask,domain].mean());means[domain]=rate;worst[domain]=np.nanmin(rates[:,domain]);values=np.sort(latency[mask,domain]);p95[domain]=values[int(np.ceil(.95*n))-1]
            denom=1+z*z/n;center=(rate+z*z/(2*n))/denom;half=z*np.sqrt(rate*(1-rate)/n+z*z/(4*n*n))/denom;wilson[domain]=[max(0.,center-half),min(1.,center+half)]
    gap=rates[:,0]-rates[:,3];passed=(counts>=2).all() and wilson[3,0]>=minimum and (gap<=gap_limit).all() and p95[3]<=budget
    manifest=dict(schema=1,seed=seed,samples=N,friction=[.4,1.2],lighting=[.5,1.5],strata=4);digest=hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode('ascii')).hexdigest()
    return dict(factors=factors,strata=strata,counts=counts,rates=rates,mean_rate=means,worst_rate=worst,p95_ms=p95,wilson=wilson,sim_real_gap=gap,decision='promote' if passed else 'hold',distribution_sha256=digest)
