"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def row(key='a',digest='a'*64,n=10,k=8,w=-1):return dict(slice=key,distribution_sha256=digest,trials=n,successes=k,worst_return=w)
def equal(m):assert m.robustness_release_gate(['a'],[row()],'a'*64,10,.8,-1)==dict(approved=True,reasons=[])
def reasons(m):assert m.robustness_release_gate(['b','a'],[row(digest='b'*64,n=5,k=1,w=-2)],'a'*64,10,.8,-1)==dict(approved=False,reasons=['a:distribution','a:trials','a:success','a:worst-return','b:missing'])
def complete(m):
 ids=['s'+str(i) for i in range(128)];records=[row(key=x) for x in ids];before=copy.deepcopy(records);assert m.robustness_release_gate(ids[::-1],records[::-1],'a'*64,10,.8,-1)['approved'];assert records==before
 r=m.robustness_release_gate(ids,[],'a'*64,1,0,-1e6);assert r['reasons']==[x+':missing' for x in sorted(ids)]
def single_failures(m):
 for key,value,reason in [('distribution_sha256','b'*64,'distribution'),('trials',11,'success'),('successes',7,'success'),('worst_return',-2,'worst-return')]:
  a=row();a[key]=value;assert m.robustness_release_gate(['a'],[a],'a'*64,10,.8,-1)['reasons']==['a:'+reason]
 assert m.robustness_release_gate(['a'],[row(n=9,k=9)],'a'*64,10,.8,-1)['reasons']==['a:trials']
def invalid(m):
 for key,value in [('trials',0),('trials',True),('successes',11),('successes',False),('worst_return',np.nan),('worst_return',10**1000),('slice','extra'),('distribution_sha256','A'*64),('extra',1)]:
  a=row();a[key]=value;rejects(lambda:m.robustness_release_gate(['a'],[a],'a'*64,10,.8,-1))
 rejects(lambda:m.robustness_release_gate(['a'],[row(),row()],'a'*64,10,.8,-1));rejects(lambda:m.robustness_release_gate(['a','a'],[],'a'*64,10,.8,-1))
 bad=row('b');bad['successes']=-1;rejects(lambda:m.robustness_release_gate(['a','b'],[row(digest='b'*64),bad],'a'*64,10,.8,-1))

TESTS=[('Exact thresholds pass', 'public', equal), ('Every independent failure reported', 'public', reasons), ('Full registry and deterministic missing evidence', 'hidden', complete), ('Isolated rejection reasons', 'hidden', single_failures), ('Validate all evidence schemas', 'hidden', invalid)]
