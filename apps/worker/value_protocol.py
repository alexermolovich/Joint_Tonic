"""Bounded data-only transport. Never deserialize pickle or Python objects."""
import base64
import math
import numpy as np

MAX_BYTES = 8 * 1024 * 1024
MAX_ITEMS = 1_000_000
MAX_DEPTH = 32
DTYPES = {np.dtype(x).str for x in ('bool', 'int8', 'int16', 'int32', 'int64',
    'uint8', 'uint16', 'uint32', 'uint64', 'float16', 'float32', 'float64', 'complex64', 'complex128')}


def encode(value, depth=0):
    if depth > MAX_DEPTH:
        raise ValueError('Value nesting exceeds protocol limit')
    if value is None or type(value) in (bool, int, str):
        return value
    if type(value) is float:
        return value if math.isfinite(value) else {'kind': 'float', 'value': str(value)}
    if isinstance(value, np.generic):
        return {'kind': 'scalar', 'value': encode(np.asarray(value), depth + 1)}
    if isinstance(value, np.ndarray):
        if value.dtype.str not in DTYPES or value.nbytes > MAX_BYTES or value.size > MAX_ITEMS:
            raise ValueError('Unsupported array dtype or size')
        return {'kind': 'array', 'dtype': value.dtype.str, 'shape': list(value.shape),
                'strides': list(value.strides),
                'data': base64.b64encode(value.tobytes(order='C')).decode('ascii')}
    if type(value) is bytes:
        return {'kind': 'bytes', 'data': base64.b64encode(value).decode('ascii')}
    if type(value) in (list, tuple):
        if len(value) > MAX_ITEMS:
            raise ValueError('Sequence exceeds protocol limit')
        return {'kind': 'tuple' if type(value) is tuple else 'list',
                'items': [encode(x, depth + 1) for x in value]}
    if type(value) is dict:
        if len(value) > MAX_ITEMS:
            raise ValueError('Mapping exceeds protocol limit')
        return {'kind': 'dict', 'items': [[encode(k, depth + 1), encode(v, depth + 1)] for k, v in value.items()]}
    raise ValueError('Unsupported value type for isolated data protocol')


def decode(value, depth=0, budget=None):
    # One shared allocation budget covers the entire message, not each leaf.
    # Strided views can require much more storage than their dense wire payload.
    if budget is None:
        budget = [2 * MAX_BYTES, MAX_ITEMS]
    budget[1] -= 1
    budget[0] -= 64 + (len(value) * 4 if type(value) is str else 0)
    if budget[0] < 0 or budget[1] < 0:
        raise ValueError('Decoded message exceeds allocation budget')
    if depth > MAX_DEPTH:
        raise ValueError('Value nesting exceeds protocol limit')
    if value is None or type(value) in (bool, int, str):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    if type(value) is not dict:
        raise ValueError('Malformed protocol value')
    kind = value.get('kind')
    if kind == 'float' and value.get('value') in ('nan', 'inf', '-inf'):
        return float(value['value'])
    if kind in ('bytes', 'array'):
        data = value.get('data')
        if not isinstance(data, str) or len(data) > (MAX_BYTES * 4 // 3 + 4):
            raise ValueError('Payload exceeds protocol limit')
        budget[0] -= len(data) * 3 // 4
        if budget[0] < 0:
            raise ValueError('Decoded message exceeds allocation budget')
        raw = base64.b64decode(data, validate=True)
        if len(raw) > MAX_BYTES:
            raise ValueError('Payload exceeds protocol limit')
        if kind == 'bytes':
            return raw
        dtype, shape = value.get('dtype'), value.get('shape')
        if dtype not in DTYPES or not isinstance(shape, list) or len(shape) > 16:
            raise ValueError('Invalid array descriptor')
        if any(type(n) is not int or not 0 <= n <= MAX_ITEMS for n in shape):
            raise ValueError('Invalid array dimensions')
        count = math.prod(shape)
        if count > MAX_ITEMS or count * np.dtype(dtype).itemsize != len(raw):
            raise ValueError('Array byte count does not match shape')
        dense = np.frombuffer(raw, dtype=dtype).reshape(shape)
        strides = value.get('strides')
        if strides is None:
            budget[0] -= len(raw)
            if budget[0] < 0:
                raise ValueError('Decoded message exceeds allocation budget')
            return dense.copy()
        if type(strides) is not list or len(strides) != len(shape) or any(type(n) is not int or abs(n) > MAX_BYTES for n in strides):
            raise ValueError('Invalid array strides')
        low = sum(min(0, (n - 1) * stride) for n, stride in zip(shape, strides)) if count else 0
        high = sum(max(0, (n - 1) * stride) for n, stride in zip(shape, strides)) if count else 0
        span = high - low + np.dtype(dtype).itemsize
        budget[0] -= span
        if span > MAX_BYTES or budget[0] < 0:
            raise ValueError('Strided array exceeds allocation budget')
        array = np.ndarray(shape, dtype=dtype, buffer=bytearray(span), strides=strides, offset=-low)
        array[...] = dense
        return array
    if kind == 'scalar':
        array = decode(value.get('value'), depth + 1, budget)
        if not isinstance(array, np.ndarray) or array.shape != ():
            raise ValueError('Invalid scalar descriptor')
        return array[()]
    items = value.get('items')
    if kind not in ('tuple', 'list', 'dict') or type(items) is not list or len(items) > MAX_ITEMS:
        raise ValueError('Malformed protocol collection')
    budget[0] -= len(items) * (160 if kind == 'dict' else 16)
    if budget[0] < 0:
        raise ValueError('Decoded message exceeds allocation budget')
    if kind == 'dict':
        result = {}
        for pair in items:
            if type(pair) is not list or len(pair) != 2:
                raise ValueError('Malformed mapping entry')
            key = decode(pair[0], depth + 1, budget)
            if type(key) not in (str, int, float, bool, tuple, bytes) or key in result:
                raise ValueError('Invalid or duplicate mapping key')
            result[key] = decode(pair[1], depth + 1, budget)
        return result
    result = [decode(x, depth + 1, budget) for x in items]
    return tuple(result) if kind == 'tuple' else result
