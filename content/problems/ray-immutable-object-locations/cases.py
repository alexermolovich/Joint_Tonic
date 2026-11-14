"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):
    np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)

def put(a,n,size=4,h='1'*64):return dict(op='put',artifact_id=a,node_id=n,sha256=h,size_bytes=size)
def evict(a,n):return dict(op='evict',artifact_id=a,node_id=n)
def example1(m):
 assert m.track_artifact_locations([put('a','n1'),put('a','n1'),put('a','n2')])==dict(artifacts=[dict(artifact_id='a',sha256='1'*64,size_bytes=4,nodes=['n1','n2'],lost=False)],physical_bytes=8)
def example2(m):
 assert m.track_artifact_locations([put('a','n1'),evict('a','n1'),evict('a','n1')])==dict(artifacts=[dict(artifact_id='a',sha256='1'*64,size_bytes=4,nodes=[],lost=True)],physical_bytes=0)
def edges(m):
 assert m.track_artifact_locations([])==dict(artifacts=[],physical_bytes=0)
 r=m.track_artifact_locations([put('a','n1',0),evict('a','n1'),put('a','n2',0),put('b','n2',0)]);assert r['physical_bytes']==0 and len(r['artifacts'])==2 and not r['artifacts'][0]['lost']
 r=m.track_artifact_locations([put('a','n1'),put('b','n1')]);assert r['physical_bytes']==8

def oracle_scale(m):
 events=[]
 for i in range(2000):events.extend([put('a'+str(i),'n1',10**12-i),put('a'+str(i),'n2',10**12-i),evict('a'+str(i),'n1')])
 before=copy.deepcopy(events);r=m.track_artifact_locations(events);assert r['physical_bytes']==sum(10**12-i for i in range(2000));assert type(r['physical_bytes']) is int
 assert [a['artifact_id'] for a in r['artifacts']]==sorted('a'+str(i) for i in range(2000));assert all(a['nodes']==['n2'] and not a['lost'] for a in r['artifacts']);assert events==before

def invalid(m):
 for events in [[evict('a','n')],[put('a','n1'),put('a','n2',5)],[put('a','n1'),evict('a','n1'),put('a','n2',4,'2'*64)],[put('a','n',-1)],[put('a','n',True)],[dict(op='drop',artifact_id='a',node_id='n')],[put('a','n',4,'not_hash')]]:reject(lambda:m.track_artifact_locations(events))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
