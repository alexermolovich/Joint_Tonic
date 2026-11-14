import numpy as np

def evaluate_smoothing_pipeline(calibration, evaluation, weights, alphas, absolute_tolerance):
    inputs=[calibration,evaluation,weights,alphas]
    for value,rank in zip(inputs,[2,2,2,1]):
        if not isinstance(value,np.ndarray) or value.dtype not in (np.dtype('float32'),np.dtype('float64')) or value.ndim!=rank or not np.isfinite(value).all() or (value.size and np.max(np.abs(value))>1000):raise ValueError('array')
    a,x,w,alphas=[value.astype(np.float64) for value in inputs]
    if not 1<=a.shape[0]<=128 or not 1<=x.shape[0]<=128 or not 1<=a.shape[1]<=64 or x.shape[1]!=a.shape[1] or w.shape[0]!=a.shape[1] or not 1<=w.shape[1]<=64 or not 1<=alphas.size<=8 or np.any(alphas<0) or np.any(alphas>1):raise ValueError('shape/alpha')
    tol=absolute_tolerance
    if type(tol) not in (int,float) or not 0<=tol<=1e6 or not np.isfinite(tol):raise ValueError('tolerance')
    am=np.maximum(np.max(np.abs(a),axis=0),1e-6);wm=np.maximum(np.max(np.abs(w),axis=1),1e-6)
    reference=x@w;all_scales=[];errors=[];row_errors=[];selected=None;best=None;chosen=0
    for k,alpha in enumerate(alphas):
        scales=np.clip(am**alpha/wm**(1-alpha),1e-6,1e6)
        xx=x/scales[None,:];ww=w*scales[:,None]
        sx=np.max(np.abs(xx),axis=1,keepdims=True)/127;sw=np.max(np.abs(ww),axis=0,keepdims=True)/127
        sx=np.where(sx==0,1.,sx);sw=np.where(sw==0,1.,sw)
        qx=np.clip(np.rint(xx/sx),-127,127).astype(np.int8);qw=np.clip(np.rint(ww/sw),-127,127).astype(np.int8)
        output=(qx.astype(np.int64)@qw.astype(np.int64))*sx*sw
        delta=output-reference;mse=float(np.mean(delta*delta))
        all_scales.append(scales);errors.append(mse);row_errors.append(np.max(np.abs(delta),axis=1))
        if best is None or mse<best:best=mse;selected=output.copy();chosen=k
    row_errors=np.array(row_errors,dtype=np.float64);accepted=np.all(row_errors<=tol,axis=1)
    return {'scales':np.array(all_scales,dtype=np.float64),'output_mse':np.array(errors,dtype=np.float64),'row_max_abs':row_errors,'accepted':accepted,'selected_index':int(chosen),'selected_output':selected,'passed':bool(accepted[chosen])}
