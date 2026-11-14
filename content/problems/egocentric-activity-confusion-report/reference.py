import math

import re

import numpy as np

def _integer(x,lo,hi):
    if type(x) is not int or not lo<=x<=hi:raise ValueError('Invalid integer')
    return x

def _int_array(x,ndim):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('int64') or x.ndim!=ndim:raise ValueError('Expected int64 array')
    return x

def _bool_array(x,shape):
    if not isinstance(x,np.ndarray) or x.dtype!=np.dtype('bool') or x.shape!=shape:raise ValueError('Expected Boolean array')
    return x

def activity_confusion_report(dataset_ids, truth, prediction, observed, num_classes):
    datasets=_int_array(dataset_ids,1);y=_int_array(truth,1);p=_int_array(prediction,1);c=_integer(num_classes,1,64)
    if len(datasets)>100000 or y.shape!=datasets.shape or p.shape!=datasets.shape or np.any(datasets<0):raise ValueError('Invalid sample layout')
    mask=_bool_array(observed,datasets.shape)
    if any(np.any(v[mask]<0) or np.any(v[mask]>=c) for v in [y,p]):raise ValueError('Invalid measured label')
    ids,indices=np.unique(datasets,return_inverse=True)
    if len(ids)*c*c>1000000:raise ValueError('Confusion output budget')
    confusion=np.zeros((len(ids),c,c),dtype=np.int64);np.add.at(confusion,(indices[mask],y[mask],p[mask]),1)
    support=confusion.sum(axis=2);recall=np.full(support.shape,np.nan,dtype=np.float64)
    np.divide(np.diagonal(confusion,axis1=1,axis2=2),support,out=recall,where=support>0)
    macro=np.array([float(np.mean(row[n>0])) if np.any(n>0) else float('nan') for row,n in zip(recall,support)],dtype=np.float64)
    return dict(dataset_ids=ids.copy(),confusion=confusion,support=support,recall=recall,macro_recall=macro)
