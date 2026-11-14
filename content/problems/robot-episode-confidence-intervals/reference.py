import numpy as np
import math

def episode_mean_interval(episodes, critical):
    if not isinstance(episodes,np.ndarray) or episodes.dtype!=np.float64 or episodes.ndim!=2 or not 2<=episodes.shape[0]<=10000 or not 1<=episodes.shape[1]<=32 or episodes.size>200000 or not np.isfinite(episodes).all() or (np.abs(episodes)>1e6).any():raise ValueError('episode metrics')
    if type(critical) not in (int,float) or not 0<=critical<=100 or not math.isfinite(critical):raise ValueError('critical multiplier')
    mean=episodes.mean(axis=0);variance=((episodes-mean)**2).sum(axis=0)/(len(episodes)-1);se=np.sqrt(variance/len(episodes))
    return dict(mean=mean,standard_error=se,interval=np.column_stack((mean-critical*se,mean+critical*se)))
