# Compute Forward Kinematics for a Serial Chain

**Status: planned.** Given joint angles, find where a planar robot's links and tool are located.

## Contract

Input `lengths` is a finite positive vector `(N,)`, in meters, with `N>=1`. Input `q` is a finite vector `(N,)`, in radians. Joint i rotates about local +z; its angle is relative to the preceding link. After that rotation, link i extends along its own +x by `lengths[i]`. The base is the world origin with identity orientation.

Return `origins` of shape `(N+1,2)`, beginning with the base and including every distal endpoint, plus a homogeneous planar tool pose `T_base_tool` of shape `(3,3)`. The final translation is the last origin; orientation is the accumulated joint angle. All values are new float64 arrays.

Reject mismatched/empty vectors, nonpositive lengths, nonfinite or complex inputs. Do not enforce joint limits or collisions in this geometry-only component. Treat the configuration as a simultaneous static state.

See [examples](examples.md), [theory](theory.md), and [hints](hints.md).
