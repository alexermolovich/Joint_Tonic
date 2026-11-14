import type { Job } from "./types";
import { itemKey, type WorkspaceChange, type WorkspaceItem } from "./workspace-protocol.ts";

export type WorkspaceState = { id: string; name: string; drafts: Record<string, string>; notes: Record<string, string>; solved: string[]; submissions: Job[]; activeJobs: Record<string, string>; bookmarks: string[] };
export type WorkspaceCache = WorkspaceState & { sync: { revisions: Record<string, number>; pending: Record<string, WorkspaceChange>; conflicts: Record<string, WorkspaceItem>; versions: Record<string,string>; archived: Record<string,{draft: string; note: string}> } };
export type RemoteWorkspace = { ownerId: string; items: WorkspaceItem[]; versions: Record<string, string>; solved: string[]; submissions: Job[]; activeJobs: Record<string, string> };
export function emptyWorkspace(): WorkspaceCache { return { id: "", name: "", drafts: {}, notes: {}, solved: [], submissions: [], activeJobs: {}, bookmarks: [], sync: { revisions: {}, pending: {}, conflicts: {}, versions: {}, archived: {} } }; }
export function parseWorkspaceCache(text: string | null): WorkspaceCache {
  const empty = emptyWorkspace();
  try {
    const raw = JSON.parse(text || "{}");
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return empty;
    const strings = (v: unknown): Record<string, string> => v && typeof v === "object" && !Array.isArray(v) ? Object.fromEntries(Object.entries(v).filter(([k, x]) => /^[a-z0-9-]+$/.test(k) && typeof x === "string")) as Record<string, string> : {};
    return { ...empty, id: typeof raw.id === "string" ? raw.id : "", name: typeof raw.name === "string" ? raw.name : "", drafts: strings(raw.drafts), notes: strings(raw.notes), activeJobs: strings(raw.activeJobs), solved: Array.isArray(raw.solved) ? raw.solved.filter((x: unknown) => typeof x === "string") : [], bookmarks: Array.isArray(raw.bookmarks) ? raw.bookmarks.filter((x: unknown) => typeof x === "string") : [], submissions: Array.isArray(raw.submissions) ? raw.submissions.filter((x: Job) => x && typeof x.id === "string" && typeof x.slug === "string" && typeof x.code === "string").slice(0,100) : [], sync: raw.sync && typeof raw.sync === "object" ? { revisions: raw.sync.revisions || {}, pending: raw.sync.pending || {}, conflicts: raw.sync.conflicts || {}, versions: raw.sync.versions || {}, archived: raw.sync.archived || {} } : empty.sync };
  } catch { return empty; }
}
export function alignWorkspaceVersions(local: WorkspaceCache, versions: Record<string,string>): WorkspaceCache {
  const next = structuredClone(local);
  for (const [slug, oldVersion] of Object.entries(local.sync.versions)) {
    if (versions[slug] === oldVersion) continue;
    if (slug in next.drafts || slug in next.notes) next.sync.archived[`${slug}@${oldVersion}`] = { draft: next.drafts[slug] || "", note: next.notes[slug] || "" };
    delete next.drafts[slug]; delete next.notes[slug]; delete next.activeJobs[slug];
    for (const [key, item] of Object.entries(next.sync.pending)) if (item.slug === slug && item.version === oldVersion) {
      delete next.sync.pending[key]; delete next.sync.conflicts[key];
      // Bookmarks belong to the problem, so preserve their pending revision
      // while rebinding the request to the new published version.
      if (item.kind === "bookmark" && versions[slug]) {
        const rebound = { ...item, version: versions[slug] };
        next.sync.pending[itemKey(rebound)] = rebound;
      }
    }
  }
  next.sync.versions = { ...versions };
  return next;
}
function assignItem(state: WorkspaceCache, item: WorkspaceItem) {
  if (item.kind === "draft") state.drafts[item.slug] = item.body;
  else if (item.kind === "note") state.notes[item.slug] = item.body;
  else state.bookmarks = item.body === "1" ? [...new Set([...state.bookmarks, item.slug])] : state.bookmarks.filter(s => s !== item.slug);
}
export function queueWorkspaceChanges(before: WorkspaceCache, after: WorkspaceState, versions: Record<string, string>): WorkspaceCache {
  const next = structuredClone({ ...after, sync: before.sync });
  for (const kind of ["draft", "note", "bookmark"] as const) {
    const oldValues = kind === "draft" ? before.drafts : kind === "note" ? before.notes : Object.fromEntries(before.bookmarks.map(s => [s,"1"]));
    const newValues = kind === "draft" ? after.drafts : kind === "note" ? after.notes : Object.fromEntries(after.bookmarks.map(s => [s,"1"]));
    for (const slug of new Set([...Object.keys(oldValues), ...Object.keys(newValues)])) {
      const body = newValues[slug] ?? (kind === "bookmark" ? "0" : "");
      if ((oldValues[slug] ?? (kind === "bookmark" ? "0" : "")) === body || !versions[slug]) continue;
      const item = { kind, slug, version: versions[slug] }; const key = itemKey(item);
      next.sync.pending[key] = { ...item, body, expectedRevision: next.sync.pending[key]?.expectedRevision ?? next.sync.revisions[key] ?? 0 };
    }
  }
  return next;
}
export function mergeRemoteWorkspace(local: WorkspaceCache, remote: RemoteWorkspace, ownerId: string): WorkspaceCache {
  if (remote.ownerId !== ownerId) throw new Error("Workspace owner mismatch.");
  const next = structuredClone(local);
  next.solved = remote.solved; next.submissions = remote.submissions;
  // The evaluator may persist only terminal jobs; retain this device's resumable
  // job IDs until polling observes completion. They never establish a score.
  next.activeJobs = { ...local.activeJobs, ...remote.activeJobs };
  for (const job of remote.submissions) if ((job.status === "completed" || job.status === "failed") && next.activeJobs[job.slug] === job.id) delete next.activeJobs[job.slug];
  for (const item of remote.items) {
    if (remote.versions[item.slug] !== item.version) continue;
    const key = itemKey(item); const pending = next.sync.pending[key];
    if (pending) {
      if (pending.body === item.body) { delete next.sync.pending[key]; delete next.sync.conflicts[key]; }
      else if (pending.expectedRevision !== item.revision) next.sync.conflicts[key] = item;
    } else assignItem(next, item);
    next.sync.revisions[key] = item.revision;
  }
  return next;
}
export function acknowledgeWorkspaceSave(local: WorkspaceCache, sent: WorkspaceChange, saved: WorkspaceItem): WorkspaceCache {
  const next = structuredClone(local); const key = itemKey(sent); const pending = next.sync.pending[key];
  next.sync.revisions[key] = saved.revision;
  if (pending?.body === sent.body) { delete next.sync.pending[key]; delete next.sync.conflicts[key]; }
  else if (pending) next.sync.pending[key] = { ...pending, expectedRevision: saved.revision };
  return next;
}
export function resolveWorkspaceConflict(local: WorkspaceCache, key: string, choice: "device" | "account"): WorkspaceCache {
  const next = structuredClone(local); const conflict = next.sync.conflicts[key]; const pending = next.sync.pending[key];
  if (!conflict || !pending) return next;
  if (choice === "account") { assignItem(next, conflict); delete next.sync.pending[key]; }
  else next.sync.pending[key] = { ...pending, expectedRevision: conflict.revision };
  next.sync.revisions[key] = conflict.revision; delete next.sync.conflicts[key];
  return next;
}
