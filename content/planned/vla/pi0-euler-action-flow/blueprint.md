---
{
  "schema_version": 1,
  "problem_id": "pi0-euler-action-flow",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Integrate an Action Flow with Euler Steps",
  "summary": "Integrate an Action Flow with Euler Steps",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2024-pi0",
    "policy-interface"
  ],
  "paper_ids": [
    "2024-pi0"
  ],
  "paper_sections": [
    "SectionIV and AppendixA-D: forward Euler inference"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "pi0-flow-action-interpolants"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.euler_action_flow",
  "physical_contract": {
    "frames": [
      "Caller-declared normalized action interface; no frame conversion"
    ],
    "units": {
      "tokens": "dimensionless integer IDs",
      "actions": "normalized Euclidean channels",
      "flow_time": "dimensionless, separate from controller timestamps"
    },
    "axes": "Shapes and ordering defined explicitly in statement.md",
    "timestamp_assumptions": "One aligned control observation per batch item; fixed horizon interval provided upstream",
    "batching": "Batch-first; empty batch supported only for token grammar tasks"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "dtype-shape-range-validation",
      "ordering",
      "noncontiguous-and-storage",
      "empty-where-supported",
      "independent-oracle",
      "realistic-scale"
    ]
  },
  "fixtures": {
    "source": "Original synthetic inputs",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded component contract inspired by the cited mechanism; no full trained policy or physical evaluation is reproduced.",
    "primary_urls": [
      "https://arxiv.org/pdf/2410.24164v4"
    ],
    "implementation_urls": []
  },
  "owners": [
    "vla_implementation"
  ],
  "reviewers": [
    "code_issue_scout"
  ]
}
---

# Integrate an Action Flow with Euler Steps

## Contract

Implement euler_action_flow(initial, times, velocity), returning (final, trace). initial is a finite NumPy float64 array(B,H,D), abs values<=1e6, with1<=B<=16,1<=H<=64,1<=D<=32. times is finite float64 shape(K+1,),1<=K<=128, starts exactly0, ends exactly1 and is strictly increasing. Require (K+1)*B*H*D<=1,000,000. Each array may be noncontiguous.

velocity is callable. At step k call it exactly once as velocity(state, float(times[k])). It returns a finite float64 ndarray with the state's exact shape and absolute entries<=1e6, interpreted as velocity in normalized action coordinates per unit dimensionless flow time. Evaluator callbacks are deterministic, do not mutate arguments and may depend on both state and time. Do not call at the final time1.

Update state <- state + (times[k+1]-times[k])*velocity(state,times[k]). Record the initial state and every updated state in trace(K+1,B,H,D). final(B,H,D) equals trace[-1] numerically but is an independent copy; neither output aliases either input or the other output. Preserve inputs. Callback outputs may alias its input, so consume them without mutation. Callback-thrown exceptions propagate unchanged.

Raise TypeError for non-array initial/times or non-callable velocity. Raise ValueError for input-contract violations or callback return-contract violations, including a non-array callback result. There is no tensor autograd, random sampling, clipping, adaptive solver, observation encoder or hardware execution. Initial noise is supplied; every output has the same normalized Euclidean action-channel semantics, frame and horizon ordering as initial. Flow time is not robot-control time. Sum of positive step sizes is1, so declared input/velocity bounds keep accumulated states finite.

## Reference and evaluator plan

Implement the declared deterministic interface, with independent fixture/oracle checks of ordering, boundaries, ownership and all documented errors. Public examples establish visible behavior; hidden cases test the same contract at additional shapes. Use the actual local bubblewrap runtime for Run and Submit. No new dependencies or external assets. Static tables and original display math provide the theory visual; synthetic fixtures are CC0-1.0.
