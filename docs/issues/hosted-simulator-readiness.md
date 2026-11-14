# Hosted simulator asks for login when no backend exists

Status: reproduced and fixed on `codex/hosted-simulator-readiness`; local issue draft. No remote GitHub issue or PR was created.

The Vercel workspace has no remote `SIMULATOR_URL` and defaults to a loopback endpoint. A signed-out frame request previously entered session verification first and returned a login error. Signing in cannot connect Vercel to the user's local MuJoCo process. The same ordering affected hosted code execution.

Proof of success: an unconfigured hosted backend returns HTTP 503 before requesting identity; configured hosted backends still reject unsigned requests; signed-out loopback simulation remains available. The simulator response identifies this specific deployment state so the UI can offer the fixed localhost Franka demo link. No service token, remote execution, tunnel, or account bypass is introduced.

The user explicitly chose to keep simulation local for now. The fix explains this boundary and preserves the independent login/account feature.

Verification: eight focused backend connection tests pass, covering readiness, local guests, configured remote authentication, URL rejection, and request limits. TypeScript validation and final UI verification are recorded in the associated PR draft.
