# Explain unavailable hosted simulation and link to the local demo

Fixes the local issue draft [hosted simulator readiness](../issues/hosted-simulator-readiness.md).

When Vercel has no configured simulator, the workspace previously told guests to sign in before discovering the missing backend. It now reports the deployment limitation immediately and links to the localhost Franka demo. Login remains available for accounts, configured hosted service authentication remains enforced, and local guest execution is unchanged.

Validation: eight focused backend tests and TypeScript validation passed; `git diff --check` is clean. No remote simulator was deployed. The parent agent should check the explicit unavailable state in the browser after merging, then publish the web-only fix. Remote GitHub PR creation is not available in this workflow; this is a reviewable local branch and PR draft.
