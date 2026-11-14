# Worked examples

## Normalize before composing

q_after=[2,0,0,0], q_before=[0,0,0,3].

Return [0,0,0,1]. An identity rotation applied after a 180° z rotation leaves it unchanged.

## Two different axes

Let s=sqrt(0.5). q_after=[s,0,0,s] is +90° about z, q_before=[s,s,0,0] is +90° about x.

Return [0.5,0.5,0.5,0.5]. A vector initially along +y first moves to +z and stays +z under the second rotation. Reversing the input order produces [0.5,0.5,-0.5,0.5], a different rotation.
