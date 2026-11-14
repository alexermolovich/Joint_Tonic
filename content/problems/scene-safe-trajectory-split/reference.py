import hashlib
import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def split_trajectories_by_scene(episode_ids, scene_ids, validation_buckets, seed):
    if type(validation_buckets) is not int or not 0 <= validation_buckets <= 10000:
        raise ValueError("validation_buckets")
    if type(seed) is not int or not 0 <= seed <= 2**32-1:
        raise ValueError("seed")
    if not isinstance(episode_ids, list) or not isinstance(scene_ids, list):
        raise ValueError("collections")
    if len(episode_ids) != len(scene_ids) or len(episode_ids) > 100000:
        raise ValueError("length")
    for names in (episode_ids, scene_ids):
        if any(not isinstance(name, str) or not _NAME.fullmatch(name) for name in names):
            raise ValueError("identifier")
    if len(set(episode_ids)) != len(episode_ids):
        raise ValueError("duplicate episode")
    decisions = {}
    result = {"train": [], "validation": []}
    for episode, scene in zip(episode_ids, scene_ids):
        if scene not in decisions:
            digest = hashlib.sha256((str(seed) + "\0" + scene).encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:8], "big") % 10000
            decisions[scene] = "validation" if bucket < validation_buckets else "train"
        result[decisions[scene]].append(episode)
    return result

