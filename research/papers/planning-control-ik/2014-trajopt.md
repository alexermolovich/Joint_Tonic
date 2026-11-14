---
{
  "schema_version": 1,
  "paper_id": "2014-trajopt",
  "title": "Motion Planning with Sequential Convex Optimization and Convex Collision Checking",
  "authors": [
    "John Schulman",
    "Yan Duan",
    "Jonathan Ho",
    "Alex Lee",
    "Ibrahim Awwal",
    "Henry Bradlow",
    "Jia Pan",
    "Sachin Patil",
    "Ken Goldberg",
    "Pieter Abbeel"
  ],
  "year": 2014,
  "venue_or_status": "International Journal of Robotics Research 33(9); DOI10.1177/0278364914528132",
  "primary_url": "https://rll.berkeley.edu/trajopt/ijrr/",
  "pdf_url": "https://rll.berkeley.edu/trajopt/ijrr/2013-IJRR-TRAJOPT.pdf",
  "local_pdf": "./2014-trajopt.pdf",
  "sha256": "38e1d0d2485dd6d7c40a160fa4e6b9aa842e50a36c9db967b47270f03870ef85",
  "bytes": 12622596,
  "pages": 16,
  "topics": [
    "trajectory optimization",
    "collision avoidance",
    "sequential convex optimization"
  ],
  "modalities": [
    "joint trajectories",
    "collision geometry"
  ],
  "track_role": "supporting",
  "open_access_status": "open-access-author-manuscript",
  "redistribution_note": "Local research reference only. Open-access source verified; downstream redistribution rights have not been audited. The PDF is not a public product asset.",
  "acquired_on": "2026-11-13",
  "source_verification": "Primary title/authors and version checked; PDF signature, all-page parser readability, first-page visual render, count and SHA-256 validated.",
  "execution_flow": {
    "title": "Selected mechanism and implementation path",
    "description": "Trajectory optimization through repeated convex approximations, trust-region control and signed-distance collision penalties, including attention to collision safety between waypoints.",
    "nodes": [
      {
        "id": "score",
        "title": "Score a trajectory",
        "detail": "Score a trajectory. See the original explanation and component status below.",
        "column": 0,
        "row": 0,
        "section": "Score a trajectory",
        "problem_slugs": [
          "planar-two-link-ik"
        ],
        "planned_problems": [
          "Build a Joint-Space Smoothness Cost"
        ]
      },
      {
        "id": "convexify",
        "title": "Linearize signed-distance penalties",
        "detail": "Linearize signed-distance penalties. See the original explanation and component status below.",
        "column": 1,
        "row": 0,
        "section": "Linearize signed-distance penalties",
        "problem_slugs": [],
        "planned_problems": [
          "Linearize a Signed-Distance Collision Penalty",
          "Bound a Sequential Convex Trust-Region Step"
        ]
      },
      {
        "id": "swept",
        "title": "Check swept motion",
        "detail": "Check swept motion. See the original explanation and component status below.",
        "column": 2,
        "row": 0,
        "section": "Check swept motion",
        "problem_slugs": [
          "segment-occupancy-cell-check"
        ],
        "planned_problems": []
      }
    ],
    "edges": [
      {
        "from": "score",
        "to": "convexify",
        "label": "validated component output"
      },
      {
        "from": "convexify",
        "to": "swept",
        "label": "validated component output"
      }
    ]
  }
}
---

## Core paper explanation

TrajOpt improves an initial motion by solving a sequence of simpler optimization problems. Each local problem approximates nonlinear costs and constraints near the current trajectory. Collision penalties and trust-region decisions help decide which candidate updates to accept. A waypoint-only check is insufficient when the robot can cross an obstacle between two safe samples.

## Execution flow

### Score a trajectory

Let $Q=(\mathbf q_0,\ldots,\mathbf q_T)$ be joint configurations, with joint coordinates and any base coordinates in explicitly declared units. A simple teaching smoothness term is

$$
J_{\mathrm{smooth}}(Q)=\sum_{t=0}^{T-1}
(\mathbf q_{t+1}-\mathbf q_t)^\top W(\mathbf q_{t+1}-\mathbf q_t).
$$

$W$ is a positive semidefinite weighting matrix chosen to make mixed channel scales meaningful. This illustrative cost is one trajectory component, not a complete reproduction of every cost configuration in the paper. [Solve Closed-Form IK for a Planar Two-Link Arm](/problems/planar-two-link-ik) is a kinematic prerequisite for constructing small synthetic robot trajectories. Planned component: **Build a Joint-Space Smoothness Cost**.

### Linearize signed-distance penalties

Let $d(\mathbf q)$ be signed separation in meters between one robot/obstacle pair, positive outside collision, and $d_{\mathrm{safe}}>0$ the required margin. A hinge penalty is

$$
\ell_{\mathrm{col}}(\mathbf q)=\max(0,d_{\mathrm{safe}}-d(\mathbf q)).
$$

At current configuration $\bar{\mathbf q}$, a first-order model is

$$
d(\bar{\mathbf q}+\Delta\mathbf q)
\approx d(\bar{\mathbf q})+
\nabla d(\bar{\mathbf q})^\top\Delta\mathbf q.
$$

The gradient's units are meters per joint-coordinate unit. Restricting the step to a trust region reduces reliance on an inaccurate local approximation. The optimization loop must compare actual improvement with predicted improvement and adjust its region or penalty strength; a convex subproblem alone is not proof that the original nonlinear constraints are satisfied.

For margin0.05m and separation0.02m, the hinge is0.03m. At separation0.08m it is zero. Planned components: **Linearize a Signed-Distance Collision Penalty** and **Bound a Sequential Convex Trust-Region Step**.

### Check swept motion

Two collision-free endpoints do not establish collision-free interpolation. With interpolation $\mathbf q(\alpha)$ for $\alpha\in[0,1]$, the desired continuous condition is

$$
\min_{\alpha\in[0,1]} d(\mathbf q(\alpha))\ge d_{\mathrm{safe}}.
$$

The paper develops convex collision-checking formulations for motion segments. A grid exercise such as **Check a Segment Against Occupancy Cells** is a simpler prerequisite with a different geometry contract; it must not be advertised as that continuous articulated-body checker.

| Stage | Evidence | Failure to detect |
|---|---|---|
| Waypoint geometry | Endpoint separation | Collision between samples |
| Local convex model | Predicted penalty decrease | Linearization error |
| Accepted motion | Rechecked true constraints | Stale scene/calibration |

[Check a Segment Against Occupancy Cells](/problems/segment-occupancy-cell-check) is now runnable. It checks closed line-segment intersections against occupied square cells in a two-dimensional grid, including boundary contact. Its unit-cell geometry and interpolation are explicit; it does not certify an articulated robot's swept volume. This is a prerequisite for understanding why collision checking must examine the path between safe endpoints.


## Why this matters on a robot

An optimizer may converge to a local result that depends on initialization, collision geometry and trust-region settings. Declare obstacle snapshots, link models, safety margins and interpolation rules. Numerical success is not permission to bypass a robot's independent safety system.

## Implement the components

The linked kinematic and grid segment-checking prerequisites are runnable. The listed optimization components remain research candidates requiring reviewed contracts and fixtures. The source PDF is an openly accessible author manuscript of the2014 journal paper; the2013 filename does not change the publication identity.


## Sources and scope

[Canonical primary record](https://rll.berkeley.edu/trajopt/ijrr/) · [Pinned openly accessible manuscript](https://rll.berkeley.edu/trajopt/ijrr/2013-IJRR-TRAJOPT.pdf). This is an original selected-mechanism explanation, not a full-text transcription. Linked exercises are identified as direct components or supporting prerequisites. Planned node titles are research/curriculum ideas, not published problems; new ideas require a reviewed blueprint before implementation. PDF provenance and reuse status are recorded above.
