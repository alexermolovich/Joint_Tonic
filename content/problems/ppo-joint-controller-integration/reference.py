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

def train_joint_controller(initial_theta,train_goals,noise,eval_goals,epochs,learning_rate,epsilon):
    theta=_array(initial_theta,1);goals=_array(train_goals,1);z=_array(noise,3);evaluation=_array(eval_goals,1);ep=_scalar(epochs,1,4,True);lr=_scalar(learning_rate,0,.01);eps=_scalar(epsilon,.05,.4)
    it,b,h=z.shape
    if theta.shape!=(2,) or not 0<=theta[0]<=2 or not -.5<=theta[1]<=.5 or not 1<=it<=8 or not 1<=b<=32 or not 1<=h<=16 or goals.shape!=(b,) or not 1<=len(evaluation)<=32 or (np.abs(goals)>1).any() or (np.abs(evaluation)>1).any() or (np.abs(z)>3).any():raise ValueError("controller fixture contract")
    history=np.empty((it+1,2));history[0]=theta;training=np.empty(it);errors=np.empty((it,len(evaluation)));returns=np.empty(it);clips=np.empty((it,ep));sigma=.2;constant=np.log(sigma*np.sqrt(2*np.pi))
    for iteration in range(it):
        q=np.zeros(b);features=np.empty((b,h,2));actions=np.empty((b,h));rewards=np.empty((b,h));old=np.empty((b,h))
        for t in range(h):
            x=np.column_stack([goals-q,np.ones(b)]);mu=x@theta;a=mu+sigma*z[iteration,:,t];q=q+.1*a
            features[:,t]=x;actions[:,t]=a;rewards[:,t]=-(q-goals)**2-.01*a*a;old[:,t]=-.5*((a-mu)/sigma)**2-constant
        training[iteration]=rewards.sum(axis=1).mean();target=np.zeros((b,h));carry=np.zeros(b)
        for t in range(h-1,-1,-1):carry=rewards[:,t]+.95*carry;target[:,t]=carry
        advantage=(target-target.mean())/np.sqrt(target.var()+1e-8)
        for epoch in range(ep):
            mu=features@theta;new=-.5*((actions-mu)/sigma)**2-constant;ratio=np.exp(new-old);outside=(ratio<1-eps)|(ratio>1+eps);clips[iteration,epoch]=outside.mean()
            active=~(((advantage>0)&(ratio>1+eps))|((advantage<0)&(ratio<1-eps)))
            gradient=(np.where(active,ratio*advantage*(actions-mu)/(sigma*sigma),0.)[:,:,None]*features).mean(axis=(0,1))
            if not np.isfinite(gradient).all():raise ValueError("nonfinite controller gradient")
            gradient/=max(1.,float(np.linalg.norm(gradient)));theta=np.clip(theta+lr*gradient,[0.,-.5],[2.,.5])
        history[iteration+1]=theta;q=np.zeros(len(evaluation));score=np.zeros(len(evaluation))
        for t in range(h):
            a=(evaluation-q)*theta[0]+theta[1];q=q+.1*a;score+=-(q-evaluation)**2-.01*a*a
        errors[iteration]=np.abs(q-evaluation);returns[iteration]=score.mean()
    return {'theta_history':history,'training_return':training,'evaluation_final_error':errors,'evaluation_return':returns,'clip_fraction':clips}
