"use client";
import { useEffect, useState } from "react";
import { getSupabaseBrowserClient } from "./supabase";
import { acknowledgeWorkspaceSave, alignWorkspaceVersions, emptyWorkspace, mergeRemoteWorkspace, parseWorkspaceCache, queueWorkspaceChanges, resolveWorkspaceConflict, type RemoteWorkspace, type WorkspaceCache, type WorkspaceState } from "./workspace-cache";
import type { WorkspaceItem } from "./workspace-protocol";
export type { WorkspaceState } from "./workspace-cache";

type SyncStatus = "loading" | "local" | "syncing" | "synced" | "offline" | "conflict" | "storage-error";
let scope: string | null = null;
let ready = false;
let versions: Record<string,string> = {};
let status: SyncStatus = "loading";
let message = "";
let generation = 0;
let controller: AbortController | null = null;
let timer: ReturnType<typeof setTimeout> | undefined;
let running = false;
let rerun = false;
const memory = new Map<string,WorkspaceCache>();
const storageFailure = "Not saved to this device: browser storage is full or unavailable. Keep this tab open and export your work from Settings.";
const storageKey = () => scope === "guest" ? "joint-tonic.workspace.v1" : `joint-tonic.workspace.v2.${scope}`;
const emit = () => { if (typeof window !== "undefined") window.dispatchEvent(new Event("jt-workspace")); };
function write(state: WorkspaceCache) {
  try { localStorage.setItem(storageKey(), JSON.stringify(state)); if (memory.delete(storageKey())) { status = scope === "guest" ? "local" : "syncing"; message = ""; } }
  catch { memory.set(storageKey(), state); status = "storage-error"; message = storageFailure; }
  emit();
}
export function readWorkspace(): WorkspaceCache {
  if (typeof window === "undefined" || !scope) return emptyWorkspace();
  if (memory.has(storageKey())) return structuredClone(memory.get(storageKey())!);
  try { return parseWorkspaceCache(localStorage.getItem(storageKey())); } catch { return emptyWorkspace(); }
}
export function setWorkspaceScope(userId: string | null, problemVersions: Record<string,string>) {
  versions = problemVersions;
  const next = userId ? `account.${userId}` : "guest";
  if (next === scope) return;
  generation++; controller?.abort(); clearTimeout(timer); running = false; rerun = false;
  scope = next; ready = !userId; status = userId ? "loading" : "local"; message = "";
  const state = userId ? alignWorkspaceVersions(readWorkspace(), versions) : readWorkspace(); if (!state.id) state.id = crypto.randomUUID();
  write(state); if (userId) scheduleWorkspaceSync(0);
}
export function updateWorkspace(fn: (state: WorkspaceState) => WorkspaceState, expectedScope = scope) {
  if (!scope || expectedScope !== scope || !ready) return readWorkspace();
  const before = readWorkspace(); const after = fn(structuredClone(before));
  const next = scope === "guest" ? { ...after, sync: before.sync } : queueWorkspaceChanges(before, after, versions);
  write(next); if (scope !== "guest") scheduleWorkspaceSync();
  return next;
}
export async function workspaceRequestHeaders(): Promise<Record<string,string>> {
  const expected = scope; const headers: Record<string,string> = { "x-workspace-id": readWorkspace().id };
  if (scope?.startsWith("account.")) {
    const client = getSupabaseBrowserClient(); const session = await client?.auth.getSession();
    if (scope !== expected || session?.error || !session?.data.session || `account.${session.data.session.user.id}` !== expected) throw new Error("Your account changed. Retry from the current workspace.");
    headers.Authorization = `Bearer ${session.data.session.access_token}`;
  }
  return headers;
}
export function scheduleWorkspaceSync(delay = 700) {
  if (!scope || scope === "guest") return;
  clearTimeout(timer); timer = setTimeout(() => { void synchronizeWorkspace(); }, delay);
}
async function synchronizeWorkspace() {
  if (!scope || scope === "guest") return;
  if (running) { rerun = true; return; }
  running = true; const revision = generation; const ownerId = scope.slice(8);
  controller = new AbortController(); const signal = AbortSignal.any([controller.signal, AbortSignal.timeout(12000)]);
  status = "syncing"; emit();
  try {
    const headers = await workspaceRequestHeaders();
    const response = await fetch("/api/workspace", { headers, signal, cache: "no-store" });
    if (!response.ok) throw new Error("Account storage unavailable. Edits remain on this device; retry when connected.");
    const remote = await response.json() as RemoteWorkspace;
    if (generation !== revision) return;
    write(mergeRemoteWorkspace(readWorkspace(), remote, ownerId));
    for (const [key, sent] of Object.entries(readWorkspace().sync.pending)) {
      if (generation !== revision) return;
      if (readWorkspace().sync.conflicts[key]) continue;
      const result = await fetch("/api/workspace", { method: "PATCH", headers: { ...headers, "Content-Type": "application/json" }, body: JSON.stringify(sent), signal });
      const saved = await result.json();
      if (generation !== revision) return;
      if (result.status === 409 && Number.isSafeInteger(saved.revision) && typeof saved.body === "string") {
        const state = readWorkspace(); state.sync.conflicts[key] = saved as WorkspaceItem; write(state); continue;
      }
      if (!result.ok) throw new Error(saved.error || "Could not save account edits. Your local copy is preserved.");
      write(acknowledgeWorkspaceSave(readWorkspace(), sent, saved as WorkspaceItem));
    }
    if (generation !== revision) return;
    const current = readWorkspace(); status = Object.keys(current.sync.conflicts).length ? "conflict" : Object.keys(current.sync.pending).length ? "syncing" : "synced";
    if (memory.has(storageKey())) { status = "storage-error"; message = storageFailure; }
    else message = "";
    if (status === "syncing") rerun = true;
  } catch (error) {
    if (generation !== revision) return;
    status = "offline"; message = error instanceof Error ? error.message : "Account sync unavailable. Your local copy is preserved.";
  } finally {
    if (generation === revision) { ready = true; running = false; if (memory.has(storageKey())) { status = "storage-error"; message = storageFailure; } emit(); if (rerun) { rerun = false; scheduleWorkspaceSync(100); } }
  }
}
export function resolveSyncConflict(key: string, choice: "device" | "account") { write(resolveWorkspaceConflict(readWorkspace(), key, choice)); scheduleWorkspaceSync(0); }
export function clearCurrentWorkspaceCache() { if (!scope) return; try { localStorage.removeItem(storageKey()); memory.delete(storageKey()); location.reload(); } catch { message = "Browser storage is unavailable. Export your work before clearing browser data."; emit(); } }
export function useWorkspace() {
  const [snapshot, setSnapshot] = useState(() => ({ state: emptyWorkspace(), ready: false, scope: null as string | null, status: "loading" as SyncStatus, message: "" }));
  useEffect(() => {
    const read = () => setSnapshot({ state: readWorkspace(), ready, scope, status, message }); read();
    const external = () => { read(); scheduleWorkspaceSync(); };
    window.addEventListener("jt-workspace", read); window.addEventListener("storage", external);
    return () => { window.removeEventListener("jt-workspace", read); window.removeEventListener("storage", external); };
  }, []);
  return { ...snapshot, update: (fn: (state: WorkspaceState) => WorkspaceState) => updateWorkspace(fn, snapshot.scope) };
}
