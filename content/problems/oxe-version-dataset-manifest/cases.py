import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def row(i='labA'):return {'dataset_id':i,'version':'1.0.0','embodiment':'fr3','content_sha256':'0'*64,'calibration_sha256':'1'*64}
def example1(m):
    import hashlib
    r=m.version_dataset_manifest([],1);text='{"datasets":[],"schema_version":1}';assert r['canonical_json']==text;assert r['sha256']==hashlib.sha256(text.encode()).hexdigest()
def example2(m):
    a=row();b=dict(reversed(list(a.items())));assert m.version_dataset_manifest([a],1)==m.version_dataset_manifest([b],1)
    b['version']='1.0.1';assert m.version_dataset_manifest([a],1)['sha256']!=m.version_dataset_manifest([b],1)['sha256'];assert a['version']=='1.0.0'
def order_and_calibration(m):
    rows=[row('lab'+str(i)) for i in range(128)];a=m.version_dataset_manifest(rows,2);b=m.version_dataset_manifest(rows[::-1],2);assert a==b
    import json
    assert [r['dataset_id'] for r in json.loads(a['canonical_json'])['datasets']]==sorted(r['dataset_id'] for r in rows)
    rows[0]['calibration_sha256']='2'*64;assert m.version_dataset_manifest(rows,2)['sha256']!=a['sha256'];assert m.version_dataset_manifest(rows,3)['sha256']!=m.version_dataset_manifest(rows,2)['sha256']
def invalid(m):
    for field,value in [('version','01.0.0'),('version','1.0'),('embodiment','bad space'),('content_sha256','A'*64),('dataset_id','')]:
        r=row();r[field]=value;bad(lambda:m.version_dataset_manifest([r],1))
    bad(lambda:m.version_dataset_manifest([row(),row()],1));bad(lambda:m.version_dataset_manifest([row()],True))
TESTS=[('Empty canonical snapshot','public',example1),('Record ordering and version','public',example2),('Full manifest ordering/calibration identity','hidden',order_and_calibration),('Invalid provenance records','hidden',invalid)]
