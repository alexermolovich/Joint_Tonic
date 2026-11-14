"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def chain(m):assert m.fuse_operator_chains([('x','input',None,(4,)),('a','scale','x',(4,)),('b','relu','a',(4,))])==[('x',),('a','b')]
def branch(m):assert m.fuse_operator_chains([('x','input',None,(4,)),('a','scale','x',(4,)),('b','relu','a',(4,)),('c','sigmoid','a',(4,))])==[('x',),('a',),('b',),('c',)]
def barriers(m):
 data=[('z','input',None,(3,)),('a','scale','z',(3,)),('q','barrier','a',(2,)),('b','relu','q',(2,)),('c','scale','b',(2,))];before=copy.deepcopy(data)
 assert m.fuse_operator_chains(data)==[('z',),('a',),('q',),('b','c')];assert data==before;assert m.fuse_operator_chains([])==[]
def scale(m):
 data=[('n0','input',None,(1,))]+[('n'+str(i),'relu','n'+str(i-1),(1,)) for i in range(1,10000)]
 assert m.fuse_operator_chains(data)==[('n0',),tuple('n'+str(i) for i in range(1,10000))]
def invalid(m):
 for x in [(),[('x','input','a',(1,))],[('x','bad',None,(1,))],[('x','relu','a',(1,))],[('x','input',None,(True,))],[('x','input',None,(4096,4096))],[('x','input',None,(1,)),('x','relu','x',(1,))],[('x','input',None,(1,)),('a','relu','x',(2,))],[('x','input',None,[1])]]:rejects(lambda:m.fuse_operator_chains(x))

TESTS=[('Fuse one unary chain', 'public', chain), ('Later consumer blocks earlier fusion', 'public', branch), ('Barriers order and empty graph', 'hidden', barriers), ('Long legal chain', 'hidden', scale), ('Typed topology and shapes', 'hidden', invalid)]
