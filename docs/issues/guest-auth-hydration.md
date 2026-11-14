# Guest workspace remounts after Auth initialization

Status: reproduced in the live browser; fixed in `codex/guest-auth-hydration`. Local issue draft only.

Opening the FR3 page and immediately selecting Simulation can be undone when Supabase confirms there is no saved session. AuthProvider changes its child key from `pending` to `guest`, remounting the entire workspace and resetting the selected pane to Code. The correct simulator-unavailable message and local demo link then exist in a hidden panel.

The regression delays Supabase's browser lock, selects Simulation before identity initialization finishes, releases the lock, waits for the guest cache to initialize, and checks that Simulation remains selected. It fails on production revision fbb38a2 with `aria-selected=false` and passes with the fix. Simulator responses are mocked; no hosted account or email is created.

Use the existing guest key during initial identity loading. Private account transitions still change the key to the actual user ID and retain workspace/cache isolation. No session validation or account ownership rule changes.
