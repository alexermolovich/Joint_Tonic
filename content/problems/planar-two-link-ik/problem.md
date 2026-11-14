# Solve Closed-Form IK for a Planar Two-Link Arm

Implement **planar_ik(L1, L2, target)**. L1 and L2 are real Python/NumPy scalars, excluding bool, in [1e-3,1e3] meters, with max(L1,L2)/min(L1,L2)<=1000. target is a finite real integer/floating array-like (2,) with per-coordinate magnitude <=1e6 meters; reject bool, complex, string and object dtypes.

Return a dict with exactly reachable (Python bool), angles (None or a new float64 (2,) array), and singular (Python bool). The shoulder angle q1 is normalized into [-pi,pi); relative elbow angle q2 is in [0,pi]. Positive angles rotate counterclockwise about base +z.

Let r=hypot(x,y). Targets below abs(L1-L2)-1e-9 or above L1+L2+1e-9 are unreachable: return False,None,False. For the tolerance band, clamp the law-of-cosines result to [-1,1] after this reachability test. For reachable targets q2=acos((r*r-L1*L1-L2*L2)/(2*L1*L2)); q1=atan2(y,x)-atan2(L2*sin(q2),L1+L2*cos(q2)). Mark singular when abs(sin(q2))<=1e-9. For exactly equal lengths and exact target [0,0], choose q1=0,q2=pi.

Raise ValueError for every documented invalid input; preserve inputs. This is one static geometric branch, without joint limits, obstacles, tool orientation or continuity across calls. Numerical results use atol=1e-7 radians and rtol=1e-7, away from tolerance-boundary classification. No simulator is required; the planned MuJoCo sidecar is separate.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-7. Masks, shapes and errors are exact.

## Worked examples

### Right-angle elbow

L1=1, L2=1, target=[1,1].

Return reachable=True, angles=[0,pi/2], singular=False. Link1 ends at [1,0], and link2 turns upward to [1,1].

### Full extension

L1=2, L2=1, target=[3,0].

Return reachable=True, angles=[0,0], singular=True. The same arm with target=[4,0] returns reachable=False, angles=None, singular=False.

### Folded equal links

L1=L2=1 and target=[0,0] returns reachable=True, angles=[0,pi], singular=True. The shoulder choice is a deterministic convention.

## Hints

1. Check the reachable annulus before evaluating inverse trigonometry.

2. Use atan2 for both the target bearing and elbow offset.

3. Treat the exactly folded equal-length origin as a declared special case.
