import numpy as np

def batch_episodes(episodes):
    if not isinstance(episodes, list) or not 1 <= len(episodes) <= 128:
        raise ValueError("episodes")
    width = None
    sizes = []
    for episode in episodes:
        if not isinstance(episode, np.ndarray) or episode.dtype != np.float64 or episode.ndim != 2:
            raise ValueError("episode dtype or rank")
        length, current_width = episode.shape
        if not 0 <= length <= 10000 or not 1 <= current_width <= 128:
            raise ValueError("episode dimensions")
        if width is not None and current_width != width:
            raise ValueError("inconsistent width")
        width = current_width
        if not np.isfinite(episode).all() or (np.abs(episode) > 1e6).any():
            raise ValueError("episode values")
        sizes.append(length)
    horizon = max(sizes)
    if len(episodes) * horizon * width > 2000000:
        raise ValueError("padded workload")
    batch = np.zeros((len(episodes), horizon, width), dtype=np.float64)
    valid = np.zeros((len(episodes), horizon), dtype=bool)
    lengths = np.array(sizes, dtype=np.int64)
    for index, episode in enumerate(episodes):
        batch[index, :sizes[index]] = episode
        valid[index, :sizes[index]] = True
    return batch, valid, lengths

