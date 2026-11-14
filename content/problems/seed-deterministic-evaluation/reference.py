import numpy as np

def seeded_episode_noise(episode_ids, root_seed, horizon, mean, std):
    if not isinstance(episode_ids,np.ndarray) or episode_ids.dtype!=np.int64 or episode_ids.ndim!=1 or len(episode_ids)>256 or (episode_ids<0).any() or (episode_ids>2**32-1).any() or len(np.unique(episode_ids))!=len(episode_ids):raise ValueError('episode IDs')
    if type(root_seed) is not int or not 0<=root_seed<=2**32-1 or type(horizon) is not int or not 0<=horizon<=256:raise ValueError('seed/horizon')
    if any(not isinstance(a,np.ndarray) or a.dtype!=np.float64 or a.ndim!=1 or not np.isfinite(a).all() or (np.abs(a)>1000).any() for a in [mean,std]) or not 1<=len(mean)<=32 or std.shape!=mean.shape or (std<0).any() or len(episode_ids)*horizon*len(mean)>1000000:raise ValueError('noise channels')
    out=np.empty((len(episode_ids),horizon,len(mean)),dtype=np.float64)
    for j,episode in enumerate(episode_ids):
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([root_seed,int(episode)])))
        out[j]=rng.standard_normal((horizon,len(mean)))*std+mean
    return out
