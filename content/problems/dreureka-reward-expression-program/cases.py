import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.evaluate_reward_expression('progress - 2 * effort',{'progress':[3,4],'effort':[1,.5]});assert_array_equal(r['reward'],[1,3]);assert r['used_features']==['effort','progress'] and r['node_count']==10

def constant(m):
    r=m.evaluate_reward_expression('1 + 2',{'x':[0,0]});assert_array_equal(r['reward'],[3,3]);assert r['used_features']==[] and r['node_count']==5

def grammar(m):
    for text in ['x[0]','x.mean()','abs(x)','x / 1','x ** 2','y','True','1e309','101','x if x else x','[x]','lambda: x','x.__class__','+'*16+'x','+'.join(['x']*50)]:bad(lambda:m.evaluate_reward_expression(text,{'x':[1]}))
    bad(lambda:m.evaluate_reward_expression('100*100*100*100',{'x':[0]}));bad(lambda:m.evaluate_reward_expression('y',{'x':np.empty(0)}))
    assert m.evaluate_reward_expression('100*100*100*100',{'x':np.empty(0)})['reward'].shape==(0,)
    assert_array_equal(m.evaluate_reward_expression('-x + (+x) + 2',{'x':[1]})['reward'],[2])

def scale(m):
    x=np.linspace(-10,10,8192)[::2];before=x.copy();r=m.evaluate_reward_expression('(x*x - 2*x) + 1',{'x':x});assert_allclose(r['reward'],(x-1)**2,atol=1e-12);assert_array_equal(x,before);assert not np.shares_memory(r['reward'],x)
    for args in [('x',{'x':[np.nan]}),('x',{'x':[1],'y':[]}),('x',{'X':[1]}),('x',{'x':[True]})]:bad(lambda:m.evaluate_reward_expression(*args))
TESTS=[('Generated arithmetic reward','public',one),('Broadcast constant','public',constant),('Allowlist depth nodes and intermediate bounds','hidden',grammar),('Polynomial oracle noncontiguous batch and invalid features','hidden',scale)]
