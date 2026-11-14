"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def launch(m):assert m.select_tensor_tile((3,3,3),[(1,1,1),(2,2,2)],48,10)==(2,2,2,144,48)
def memory(m):
 assert m.select_tensor_tile((3,3,3),[(1,1,1),(2,2,2)],47,10)==(1,1,1,297,12)
 assert m.select_tensor_tile((3,3,3),[(1,1,1)],11,10) is None
def tie(m):
 assert m.select_tensor_tile((1,1,1),[(2,1,1),(1,2,1),(1,1,2)],100,0)==(1,1,2,2,20)
 assert m.select_tensor_tile((1,1,1),[(256,256,256)],2**31,10**9)==(256,256,256,1016777216,786432)
def oracle(m):
 import itertools,math
 candidates=list(itertools.product(range(1,9),repeat=3));before=candidates.copy();shape=(37,23,19);rows=[]
 for a,b,c in candidates:
  footprint=4*(a*b+a*c+b*c)
  if footprint<=300:rows.append((math.ceil(37/a)*math.ceil(23/b)*math.ceil(19/c)*(a*b*c+17),footprint,a,b,c))
 best=min(rows);assert m.select_tensor_tile(shape,candidates,300,17)==(*best[2:],best[0],best[1]);assert candidates==before
def invalid(m):
 for a in [((0,1,1),[(1,1,1)],100,0),((1,1,1),[],100,0),((1,1,1),[(1,1,1)]*2,100,0),((1,1,1),[(True,1,1)],100,0),((1,1,1),[(257,1,1)],100,0),((1,1,1),[(1,1,1)],True,0),((1,1,1),[(1,1,1)],100,-1)]:rejects(lambda:m.select_tensor_tile(*a))

TESTS=[('Launch versus padding', 'public', launch), ('Memory boundary and no feasible tile', 'public', memory), ('Deterministic ties and large cost', 'hidden', tie), ('Independent exhaustive candidate score', 'hidden', oracle), ('Malformed complete search space', 'hidden', invalid)]
