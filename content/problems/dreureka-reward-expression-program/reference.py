import numpy as np

def _array(value, ndim=None, kind="real"):
    try: a=np.asarray(value)
    except (ValueError,TypeError,OverflowError) as e: raise ValueError("invalid array") from e
    if ndim is not None and a.ndim!=ndim: raise ValueError("invalid rank")
    if a.size>1000000: raise ValueError("array too large")
    if kind=="bool":
        if a.dtype.kind!='b': raise ValueError("boolean array required")
        return a.copy()
    if kind=="int":
        if a.dtype.kind not in 'iu': raise ValueError("integer array required")
    elif a.dtype.kind not in 'iuf': raise ValueError("real numeric array required")
    if not np.isfinite(a).all() or (np.abs(a.astype(np.float64))>1e6).any(): raise ValueError("invalid numeric values")
    return a.astype(np.int64 if kind=="int" else np.float64)

def _scalar(x,low=0,high=1e6,integer=False):
    if isinstance(x,(bool,np.bool_)) or not isinstance(x,(int,float,np.integer,np.floating)): raise ValueError("numeric scalar required")
    if integer and not isinstance(x,(int,np.integer)): raise ValueError("integer scalar required")
    if not low<=x<=high or not np.isfinite(x): raise ValueError("scalar outside bounds")
    return int(x) if integer else float(x)

def evaluate_reward_expression(expression,features):
    import ast,re
    if type(expression) is not str or not 1<=len(expression)<=512 or type(features) is not dict or not 1<=len(features)<=16:raise ValueError("expression metadata")
    arrays={}
    for name,value in features.items():
        if type(name) is not str or re.fullmatch(r'[a-z][a-z0-9_]{0,31}',name) is None:raise ValueError("feature name")
        x=_array(value,1)
        if len(x)>4096 or (np.abs(x)>100).any():raise ValueError("feature bound")
        arrays[name]=x
    sizes={len(a) for a in arrays.values()}
    if len(sizes)!=1:raise ValueError("feature batch")
    n=sizes.pop()
    try:tree=ast.parse(expression,mode='eval')
    except (SyntaxError,ValueError,RecursionError) as e:raise ValueError("expression syntax") from e
    nodes=list(ast.walk(tree))
    if len(nodes)>128:raise ValueError("node limit")
    names=set()
    def inspect(node):
        if isinstance(node,ast.Constant):
            if type(node.value) not in (int,float) or not -100<=node.value<=100:raise ValueError("literal")
            return 1
        if isinstance(node,ast.Name):
            if node.id not in arrays:raise ValueError("unknown feature")
            names.add(node.id);return 1
        if isinstance(node,ast.BinOp) and type(node.op) in (ast.Add,ast.Sub,ast.Mult):depth=1+max(inspect(node.left),inspect(node.right))
        elif isinstance(node,ast.UnaryOp) and type(node.op) in (ast.UAdd,ast.USub):depth=1+inspect(node.operand)
        else:raise ValueError("unsupported syntax")
        if depth>16:raise ValueError("depth limit")
        return depth
    inspect(tree.body)
    def evaluate(node):
        if isinstance(node,ast.Constant):out=np.full(n,float(node.value))
        elif isinstance(node,ast.Name):out=arrays[node.id].copy()
        elif isinstance(node,ast.UnaryOp):
            child=evaluate(node.operand);out=-child if isinstance(node.op,ast.USub) else child
        else:
            left=evaluate(node.left);right=evaluate(node.right);out=left+right if isinstance(node.op,ast.Add) else left-right if isinstance(node.op,ast.Sub) else left*right
        if not np.isfinite(out).all() or (np.abs(out)>1e6).any():raise ValueError("intermediate bound")
        return out
    return {'reward':evaluate(tree.body),'used_features':sorted(names),'node_count':len(nodes)}
