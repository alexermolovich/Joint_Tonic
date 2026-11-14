import numpy as np
import math
import re

def sample_visual_scenarios(count, seed, textures, brightness, yaw, distractors):
    if type(count) is not int or not 0<=count<=10000 or type(seed) is not int or not 0<=seed<=2**32-1:raise ValueError('sampling parameters')
    if type(textures) is not list or not 1<=len(textures)<=64 or any(type(t) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',t) is None for t in textures) or len(set(textures))!=len(textures):raise ValueError('texture IDs')
    for bounds,lo,hi in [(brightness,0,10),(yaw,-math.pi,math.pi)]:
        if type(bounds) is not tuple or len(bounds)!=2 or any(type(x) not in (int,float) or not lo<=x<=hi or not math.isfinite(x) for x in bounds) or bounds[0]>bounds[1]:raise ValueError('physical interval')
    if type(distractors) is not tuple or len(distractors)!=2 or any(type(x) is not int for x in distractors) or not 0<=distractors[0]<=distractors[1]<=100:raise ValueError('count interval')
    u=np.random.Generator(np.random.PCG64(seed)).random((count,4))
    return dict(texture=[textures[int(v*len(textures))] for v in u[:,0]],brightness=brightness[0]+u[:,1]*(brightness[1]-brightness[0]),yaw=yaw[0]+u[:,2]*(yaw[1]-yaw[0]),distractors=distractors[0]+np.floor(u[:,3]*(distractors[1]-distractors[0]+1)).astype(np.int64))
