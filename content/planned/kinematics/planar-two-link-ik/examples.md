# Worked examples

## Right-angle elbow

L1=1, L2=1, target=[1,1].

Return reachable=True, angles=[0,pi/2], singular=False. Link1 ends at [1,0], and link2 turns upward to [1,1].

## Full extension

L1=2, L2=1, target=[3,0].

Return reachable=True, angles=[0,0], singular=True. The same arm with target=[4,0] returns reachable=False, angles=None, singular=False.

## Folded equal links

L1=L2=1 and target=[0,0] returns reachable=True, angles=[0,pi], singular=True. The shoulder choice is a deterministic convention.
