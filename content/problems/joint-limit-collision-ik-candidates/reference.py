import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def select_safe_ik_candidate(lengths, candidates, joint_limits, obstacles, target, margin):
    L,qs,limits,obs,g,m=map(_real,(lengths,candidates,joint_limits,obstacles,target,margin))
    if L.shape!=(2,) or np.any(L<1e-9) or qs.ndim!=2 or qs.shape[1]!=2 or len(qs)>1000 or limits.shape!=(2,2) or np.any(limits[:,0]>limits[:,1]) or obs.ndim!=2 or obs.shape[1]!=3 or len(obs)>100 or np.any(obs[:,2]<0) or g.shape!=(2,) or m.ndim!=0 or m<0: raise ValueError("Invalid IK candidate contract")
    best=None
    for i,q in enumerate(qs):
        if np.any(q<limits[:,0]) or np.any(q>limits[:,1]): continue
        elbow=L[0]*np.array([np.cos(q[0]),np.sin(q[0])]); tool=elbow+L[1]*np.array([np.cos(q.sum()),np.sin(q.sum())]); collision=False
        for a,b in [(np.zeros(2),elbow),(elbow,tool)]:
            segment=b-a; length2=segment@segment
            if length2==0: distance=np.linalg.norm(obs[:,:2]-a,axis=1)
            else:
                u=np.clip((obs[:,:2]-a)@segment/length2,0,1); distance=np.linalg.norm(a+u[:,None]*segment-obs[:,:2],axis=1)
            if np.any(distance<=obs[:,2]+m): collision=True; break
        if collision: continue
        error=float(np.linalg.norm(tool-g))
        if best is None or error<best['error']: best={'index':i,'q':q.copy(),'point':tool.copy(),'error':error}
    return best
