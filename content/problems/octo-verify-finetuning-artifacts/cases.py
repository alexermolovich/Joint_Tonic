import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def fixture():return [{'name':'adapter.up','shape':[2,3],'trainable':True}]
def one(m):
    r=m.verify_finetuning(fixture(),[],['adapter'],'0'*64);assert r['trainable_count']==6 and r['missing_artifacts']==['adapter.up'] and not r['ready']
def full(m):assert m.verify_finetuning(fixture(),[{'name':'adapter.up','shape':[2,3],'base_sha256':'0'*64}],['adapter'],'0'*64)['ready']
def scale(m):
    p=[{'name':f'adapter.p{i}','shape':[64,32],'trainable':i%2==0} for i in range(256)];a=[{'name':v['name'],'shape':v['shape'],'base_sha256':'0'*64} for v in p if v['trainable']];r=m.verify_finetuning(p,a,['adapter'],'0'*64);assert r['total_count']==256*2048 and r['trainable_count']==128*2048 and r['ready']
    p=[{'name':'adapterevil.up','shape':[1],'trainable':True},{'name':'base','shape':[2],'trainable':False}];a=[{'name':'base','shape':[2],'base_sha256':'1'*64}];r=m.verify_finetuning(p,a,['adapter'],'0'*64);assert r['unexpected_trainable']==['adapterevil.up'] and r['frozen_artifacts']==['base'] and r['mismatched_base']==['base'];assert m.verify_finetuning([],[],['a'],'0'*64)['ready']
def invalid(m):
    for p,a,pre,h in [(fixture(),[],['adapter'],'X'*64),([{'name':'a','shape':[True],'trainable':True}],[],['a'],'0'*64),(fixture(),[{'name':'no','shape':[1],'base_sha256':'0'*64}],['adapter'],'0'*64)]:bad(lambda:m.verify_finetuning(p,a,pre,h))
TESTS=[('Missing learned weights','public',one),('Complete adapter artifact','public',full),('Scale namespace boundaries and base identity','hidden',scale),('Malformed artifacts','hidden',invalid)]
