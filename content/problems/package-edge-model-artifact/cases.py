"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


import hashlib,json
META=dict(format='onnx',runtime='cpu_v1',input_shape=(1,3),input_dtype='float32',calibration_sha256='a'*64)
def package(m):
 r=m.package_edge_model(b'abc',META,hashlib.sha256(b'abc').hexdigest());assert r['size_bytes']==3 and r['model_sha256']=='ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
 payload=b'{"metadata":{"calibration_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","format":"onnx","input_dtype":"float32","input_shape":[1,3],"runtime":"cpu_v1"},"model_sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","size_bytes":3}'
 assert r['manifest_sha256']==hashlib.sha256(payload).hexdigest()
def mismatch(m):rejects(lambda:m.package_edge_model(b'abc',META,'0'*64))
def order_storage(m):
 meta=copy.deepcopy(META);before=copy.deepcopy(meta);a=m.package_edge_model(b'x',meta,hashlib.sha256(b'x').hexdigest());b=m.package_edge_model(b'x',dict(reversed(list(meta.items()))),hashlib.sha256(b'x').hexdigest())
 assert a==b and meta==before and a['metadata'] is not meta and type(a['metadata']['input_shape']) is tuple
 a['metadata']['runtime']='changed';assert meta==before
 meta['calibration_sha256']='b'*64;c=m.package_edge_model(b'x',meta,hashlib.sha256(b'x').hexdigest());assert b['manifest_sha256']!=c['manifest_sha256']
def scale(m):
 data=bytes(range(256))*4096;r=m.package_edge_model(data,META,hashlib.sha256(data).hexdigest());assert r['size_bytes']==1048576
 rejects(lambda:m.package_edge_model(data+b'x',META,hashlib.sha256(data+b'x').hexdigest()))
def invalid(m):
 for key,value in [('format',[]),('format','pt'),('runtime','CPU'),('input_shape',[1,3]),('input_shape',(True,)),('input_shape',(4096,4096)),('input_dtype',None),('calibration_sha256','A'*64),('extra',1)]:
  meta=copy.deepcopy(META);meta[key]=value;rejects(lambda:m.package_edge_model(b'a',meta,hashlib.sha256(b'a').hexdigest()))
 for data,digest in [(b'','0'*64),(bytearray(b'a'),'0'*64),(b'a','x'*64),(b'a',None)]:rejects(lambda:m.package_edge_model(data,META,digest))

TESTS=[('Canonical package identity', 'public', package), ('Reject mismatched model bytes', 'public', mismatch), ('Metadata order independence and storage', 'hidden', order_storage), ('One MiB model boundary', 'hidden', scale), ('Invalid package contracts', 'hidden', invalid)]
