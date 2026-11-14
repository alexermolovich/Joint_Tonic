# Check a Motion Segment Against Inflated Obstacles

**Status: planned; no runnable implementation yet.**

A planner proposes moving the robot center along a straight segment. Determine whether that entire segment remains outside every axis-aligned obstacle, including a declared clearance.

## Contract

Planned function: check_segment(start, end, obstacles, clearance).

Start/end are finite 2-D world coordinates in meters. Obstacles is a list of closed boxes [xmin,ymin,xmax,ymax] with non-reversed finite bounds. Clearance is finite and nonnegative. Expand each box by clearance in both x and y, then test the segment against those expanded boxes. Touching a boundary counts as collision.

Return free, first_obstacle, and entry_t. A free segment has first_obstacle=None and entry_t=None. Otherwise return the earliest intersected original obstacle index and its first segment parameter in [0,1]; equal entry parameters prefer the lower index. A zero-length segment is a point-in-box test.

## Scope and assessment

The expansion defines an L-infinity clearance envelope; it conservatively bounds a disk but does not compute exact circular clearance around corners. This is translational 2-D motion, not arm self-collision or swept rotation. Grade crossing, parallel, touching, start-inside, empty obstacles, and zero-length cases. See [examples.md](examples.md). Status: planned.

