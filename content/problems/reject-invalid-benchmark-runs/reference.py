import math
import re

def benchmark_run_rejections(run, protocol):
    run_fields={'scenario','model_sha256','expected_queries','completed_queries','failed_queries','duration_ns','quality'}
    protocol_fields={'scenario','model_sha256','min_queries','min_duration_ns','min_quality'}
    if type(run) is not dict or set(run)!=run_fields or type(protocol) is not dict or set(protocol)!=protocol_fields:raise ValueError("schema")
    for record in (run,protocol):
        if type(record['scenario']) is not str or record['scenario'] not in ('single_stream','server'):raise ValueError("scenario")
        if type(record['model_sha256']) is not str or re.fullmatch('[0-9a-f]{64}',record['model_sha256']) is None:raise ValueError("hash")
    def integer(v,lo,hi):
        if type(v) is not int or not lo<=v<=hi:raise ValueError("counter/duration")
    for key in ('expected_queries','completed_queries','failed_queries'):integer(run[key],0,10**9)
    integer(run['duration_ns'],0,2**63-1);integer(protocol['min_queries'],1,10**9);integer(protocol['min_duration_ns'],1,2**63-1)
    for v in (run['quality'],protocol['min_quality']):
        if type(v) not in (int,float) or not 0<=v<=1 or not math.isfinite(v):raise ValueError("quality")
    c=run['completed_queries'];f=run['failed_queries'];e=run['expected_queries']
    if c+f>e:raise ValueError("counter accounting")
    reasons=[]
    for bad,label in [(run['scenario']!=protocol['scenario'],'scenario'),(run['model_sha256']!=protocol['model_sha256'],'model'),(c+f<e,'incomplete'),(f>0,'failed_queries'),(c<protocol['min_queries'],'insufficient_queries'),(run['duration_ns']<protocol['min_duration_ns'],'insufficient_duration'),(run['quality']<protocol['min_quality'],'quality')]:
        if bad:reasons.append(label)
    return sorted(reasons)
