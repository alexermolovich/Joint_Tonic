import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Scalar outside contract")
    return float(x)

def _tree_costs(parents,edges):
    n=len(parents);children=[[] for _ in range(n)]
    for i in range(1,n):children[int(parents[i])].append(i)
    order=[0];costs=np.zeros(n)
    for i in order:
        for child in children[i]:costs[child]=costs[i]+edges[child];order.append(child)
    if len(order)!=n:raise ValueError("tree cycle or disconnection")
    return costs,children

def rewire_tree(parents,edge_costs,vertex,new_parent,connection_cost,feasible):
    p=_array(parents,1,"i");e=_array(edge_costs,1);n=len(p);c=_scalar(connection_cost,0,1e6)
    if not 2<=n<=10000 or e.shape!=p.shape or p[0]!=-1 or e[0]!=0 or np.any(e<0) or np.any((p[1:]<0)|(p[1:]>=n)) or np.any(p[1:]==np.arange(1,n)):raise ValueError("tree contract")
    if type(vertex) is not int or not 1<=vertex<n or type(new_parent) is not int or not 0<=new_parent<n or type(feasible) is not bool:raise ValueError("rewire arguments")
    costs,children=_tree_costs(p,e);subtree=[vertex];descendant=np.zeros(n,dtype=bool)
    for i in subtree:
        descendant[i]=True;subtree.extend(children[i])
    changed=bool(feasible and not descendant[new_parent] and costs[new_parent]+c<costs[vertex]);outp=p.copy();oute=e.copy()
    if changed:
        outp[vertex]=new_parent;oute[vertex]=c;costs,_=_tree_costs(outp,oute)
    return dict(parents=outp,edge_costs=oute,root_costs=costs,changed=changed)
