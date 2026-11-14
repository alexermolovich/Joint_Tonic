from copy import deepcopy
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

import hashlib

def interleaved(m):
    assert m.split_trajectories_by_scene(["ep_a","ep_b","ep_c","ep_d"],["kitchen","office","kitchen","warehouse"],5000,7)=={"train":["ep_a","ep_c"],"validation":["ep_b","ep_d"]}

def threshold_boundary(m):
    assert m.split_trajectories_by_scene(["trial_a","trial_b"],["office","office"],2001,7)=={"train":["trial_a","trial_b"],"validation":[]}
    assert m.split_trajectories_by_scene(["trial_a","trial_b"],["office","office"],2002,7)=={"train":[],"validation":["trial_a","trial_b"]}

def empty_and_extremes(m):
    assert m.split_trajectories_by_scene([],[],5000,7)=={"train":[],"validation":[]}
    assert m.split_trajectories_by_scene(["x"],["s"],0,0)=={"train":["x"],"validation":[]}
    assert m.split_trajectories_by_scene(["x"],["s"],10000,2**32-1)=={"train":[],"validation":["x"]}

def malformed(m):
    for args in [((),[],0,0),([],(),0,0),(["a"],[],0,0),(["a","a"],["s","s"],0,0),
                 (["Bad"],["s"],0,0),(["a"],["s\0x"],0,0),([1],["s"],0,0),
                 (["a"],["s"],True,0),(["a"],["s"],10001,0),(["a"],["s"],-1,0),
                 (["a"],["s"],0,True),(["a"],["s"],0,-1),(["a"],["s"],0,2**32),
                 (["a"],["s"],np.int64(1),0),(["a"],["s"],0,10**1000)]:
        invalid(lambda: m.split_trajectories_by_scene(*args))

def independent_protocol(m):
    ids=[f"e{i}" for i in range(200)];scenes=[f"s{i%17}" for i in range(200)]
    seed=2**32-1;threshold=6000
    # Hex-prefix conversion is independent of the reference's byte decoder.
    buckets={s:int(hashlib.sha256(f"{seed}\x00{s}".encode()).hexdigest()[:16],16)%10000 for s in set(scenes)}
    expected={"train":[e for e,s in zip(ids,scenes) if buckets[s]>=threshold],
              "validation":[e for e,s in zip(ids,scenes) if buckets[s]<threshold]}
    saved=deepcopy((ids,scenes));out=m.split_trajectories_by_scene(ids,scenes,threshold,seed)
    assert out==expected and (ids,scenes)==saved
    assert out["train"] is not ids and out["validation"] is not ids and out["train"] is not out["validation"]
    rev=m.split_trajectories_by_scene(ids[::-1],scenes[::-1],threshold,seed)
    assert rev=={key:value[::-1] for key,value in out.items()}

def scale_scene_isolation(m):
    ids=[f"e{i}" for i in range(100000)];scenes=["kitchen" if i%2 else "office" for i in range(100000)]
    out=m.split_trajectories_by_scene(ids,scenes,5000,7)
    assert out=={"train":ids[1::2],"validation":ids[::2]}
    invalid(lambda: m.split_trajectories_by_scene(ids+["overflow"],scenes+["office"],5000,7))

TESTS=[("Interleaved scene grouping","public",interleaved),("Strict bucket threshold","public",threshold_boundary),("Empty and extreme thresholds","public",empty_and_extremes),
       ("Malformed split inputs","hidden",malformed),("Independent protocol order and storage","hidden",independent_protocol),("Large scene-isolated split","hidden",scale_scene_isolation)]

