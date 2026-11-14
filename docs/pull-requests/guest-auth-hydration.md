# Preserve the guest's selected pane during Auth initialization

Fixes [the guest hydration issue](../issues/guest-auth-hydration.md).

Keep the guest child identity stable while Supabase initializes and confirms a signed-out session. This prevents an immediate Simulation click from resetting to Code. Real user identity changes still remount the workspace to separate account data.

Verification: the new delayed-Auth browser regression reproduced the failure on the deployed revision and passed against the fix. TypeScript validation and diff checks passed. Existing account-sync/conflict/account-switch browser assertions completed successfully, but its final no-console-errors assertion failed because the isolated worktree lacks generated Monaco assets (six editor load events). Run that existing test on the main development server with prepared Monaco assets for a clean browser result. No remote GitHub issue or PR was created; this is a local issue-linked fix branch.
