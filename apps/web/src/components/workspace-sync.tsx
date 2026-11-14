"use client";
import { useEffect } from "react";
import Link from "next/link";
import { resolveSyncConflict, scheduleWorkspaceSync, useWorkspace } from "@/lib/local-workspace";
import "./workspace-sync.css";

export function WorkspaceSyncEvents() {
  useEffect(() => {
    const refresh = () => { if (document.visibilityState !== "hidden") scheduleWorkspaceSync(0); };
    window.addEventListener("focus", refresh); window.addEventListener("online", refresh);
    const interval = setInterval(refresh, 30000);
    return () => { clearInterval(interval); window.removeEventListener("focus", refresh); window.removeEventListener("online", refresh); };
  }, []);
  return null;
}
export function WorkspaceSyncStatus({ detailed = false }: { detailed?: boolean }) {
  const { state, status, message, scope } = useWorkspace();
  const labels = { loading: "Loading saved work…", local: "Saved on this device", syncing: "Syncing account…", synced: "Saved to your account", offline: "Saved on this device · sync unavailable", conflict: "Edits need review", "storage-error": "Not saved to this device · export your work" };
  if (!detailed) return <span className="workspace-save" role="status">{labels[status]}{status === "conflict" && <> · <Link href="/settings">Review</Link></>}</span>;
  return <section className="settings-card"><h2>Saved workspace</h2><p role="status">{labels[status]}</p><p>{scope?.startsWith("account.") ? "Drafts, notes and bookmarks sync to this account. Submission history and solved progress come from verified server records. Guest work stays separate." : "Signed-out work stays in this browser. Sign in to use a separate account workspace across devices."}</p>{message && <p role="alert">{message}</p>}{scope?.startsWith("account.") && <button className="button secondary" onClick={() => scheduleWorkspaceSync(0)}>Retry sync</button>}{Object.entries(state.sync.conflicts).map(([key, remote]) => <details key={key} className="settings-card" open><summary>{remote.kind}: {remote.slug} has edits on another device</summary><p>Your version is preserved locally. Choose which version to keep in your account.</p><details><summary>Account version</summary><pre>{remote.body}</pre></details><details><summary>This device’s version</summary><pre>{state.sync.pending[key]?.body}</pre></details><button className="button secondary" onClick={() => resolveSyncConflict(key, "account")}>Use account version</button><button className="button secondary" onClick={() => resolveSyncConflict(key, "device")}>Keep this device’s version</button></details>)}{Object.entries(state.sync.archived).map(([key, archive])=><details key={key}><summary>Preserved work from {key}</summary><p>This older content version is kept locally for export and is not applied to the current problem.</p><pre>{archive.draft}</pre><pre>{archive.note}</pre></details>)}</section>;
}
