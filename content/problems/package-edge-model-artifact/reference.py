import hashlib
import json
import math
import re
import copy

def package_edge_model(model_bytes, metadata, expected_sha256):
    def digest(x):return type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None
    if type(model_bytes) is not bytes or not 1<=len(model_bytes)<=1048576 or not digest(expected_sha256):raise ValueError('model bytes/digest')
    actual=hashlib.sha256(model_bytes).hexdigest()
    if actual!=expected_sha256:raise ValueError('model digest mismatch')
    if type(metadata) is not dict or set(metadata)!=set(['format','runtime','input_shape','input_dtype','calibration_sha256']):raise ValueError('metadata schema')
    shape=metadata['input_shape'];runtime=metadata['runtime']
    if type(metadata['format']) is not str or metadata['format'] not in ('onnx','tflite') or type(metadata['input_dtype']) is not str or metadata['input_dtype'] not in ('float32','uint8'):raise ValueError('format/dtype')
    if type(runtime) is not str or re.fullmatch(r'[a-z][a-z0-9_.-]{0,63}',runtime) is None or not digest(metadata['calibration_sha256']):raise ValueError('runtime/calibration')
    if type(shape) is not tuple or not 1<=len(shape)<=4 or any(type(d) is not int or not 1<=d<=4096 for d in shape) or math.prod(shape)>1000000:raise ValueError('input shape')
    result=dict(model_sha256=actual,size_bytes=len(model_bytes),metadata=copy.deepcopy(metadata))
    payload=json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('utf-8')
    result['manifest_sha256']=hashlib.sha256(payload).hexdigest()
    return result
