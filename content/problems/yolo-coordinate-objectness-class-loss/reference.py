import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def yolo_loss(predicted_boxes, confidence, class_probabilities, target_boxes, target_labels, responsible, target_iou):
    p=_array(predicted_boxes,4);c=_array(confidence,3);a=_array(class_probabilities,3);t=_array(target_boxes,3);l=_array(target_labels,2,"i");r=_array(responsible,2,"i");iou=_array(target_iou,2)
    s=p.shape[0];b=p.shape[2]
    if not 1<=s<=16 or p.shape[1]!=s or not 1<=b<=8 or p.shape[3]!=4 or c.shape!=(s,s,b) or a.shape[:2]!=(s,s) or not 1<=a.shape[2]<=64 or t.shape!=(s,s,4) or any(x.shape!=(s,s) for x in (l,r,iou)):raise ValueError("Loss shapes")
    for boxes in (p,t):
        if np.any(boxes[...,:2]<0) or np.any(boxes[...,:2]>1) or np.any(boxes[...,2:]<1e-6) or np.any(boxes[...,2:]>1):raise ValueError("Boxes")
    if any(np.any(x<0) or np.any(x>1) for x in (c,a,iou)) or not np.allclose(a.sum(2),1,rtol=0,atol=1e-8) or np.any(l< -1) or np.any(l>=a.shape[2]):raise ValueError("Class/confidence")
    occupied=l>=0
    if np.any(r[~occupied]!=-1) or np.any(r[occupied]<0) or np.any(r[occupied]>=b):raise ValueError("Responsibility")
    rows,cols=np.nonzero(occupied);chosen=r[rows,cols];pred=p[rows,cols,chosen];truth=t[rows,cols]
    coordinate=5*np.sum((pred[:,:2]-truth[:,:2])**2)+5*np.sum((np.sqrt(pred[:,2:])-np.sqrt(truth[:,2:]))**2)
    resp_mask=np.zeros_like(c,dtype=bool);resp_mask[rows,cols,chosen]=True
    objectness=np.sum((c[rows,cols,chosen]-iou[rows,cols])**2)+.5*np.sum(c[~resp_mask]**2)
    onehot=np.eye(a.shape[2])[l[rows,cols]];classification=np.sum((a[rows,cols]-onehot)**2)
    return dict(coordinate=float(coordinate),objectness=float(objectness),classification=float(classification),total=float(coordinate+objectness+classification))
