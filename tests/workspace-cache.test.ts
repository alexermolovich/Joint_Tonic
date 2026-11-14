import test from "node:test";
import assert from "node:assert/strict";
import { emptyWorkspace, alignWorkspaceVersions, queueWorkspaceChanges, mergeRemoteWorkspace, acknowledgeWorkspaceSave, resolveWorkspaceConflict, parseWorkspaceCache, type RemoteWorkspace } from "../apps/web/src/lib/workspace-cache.ts";
import { itemKey, parseWorkspaceChange } from "../apps/web/src/lib/workspace-protocol.ts";

const versions = { frames: "1.0.0", camera: "2.0.0" };
const remote = (items: RemoteWorkspace["items"] = []): RemoteWorkspace => ({ ownerId: "account-a", items, versions, solved: [], submissions: [], activeJobs: {} });
const draft = { kind: "draft" as const, slug: "frames", version: "1.0.0", body: "account text", revision: 4 };
test("editable payload cannot claim owner, solves, submissions, or grading", () => {
  const valid = { ...draft, expectedRevision: 4 }; delete (valid as Partial<typeof draft>).revision;
  assert.equal(parseWorkspaceChange(valid).expectedRevision, 4);
  for (const extra of [{ userId: "other" }, { solved: ["frames"] }, { passed: true }, { submissions: [] }]) assert.throws(() => parseWorkspaceChange({ ...valid, ...extra }));
  for (const change of [{ ...valid, body: "é".repeat(50001) }, { ...valid, expectedRevision: -1 }, { ...valid, kind: "bookmark", body: "yes" }]) assert.throws(() => parseWorkspaceChange(change));
});
test("remote owner mismatch is rejected without mutating local data", () => {
  const local = emptyWorkspace(); local.notes.frames = "private A";
  assert.throws(() => mergeRemoteWorkspace(local, { ...remote(), ownerId: "account-b" }, "account-a"));
  assert.equal(local.notes.frames, "private A");
});
test("clean fields receive remote text while verified records replace local claims", () => {
  const local = emptyWorkspace(); local.solved = ["forged"];
  const result = mergeRemoteWorkspace(local, remote([draft]), "account-a");
  assert.equal(result.drafts.frames, "account text"); assert.deepEqual(result.solved, []); assert.deepEqual(local.solved, ["forged"]);
  assert.equal(result.sync.revisions[itemKey(draft)], 4);
});
test("new edits during an in-flight save survive acknowledgement and advance the base revision", () => {
  const base = mergeRemoteWorkspace(emptyWorkspace(), remote([draft]), "account-a");
  const first = queueWorkspaceChanges(base, { ...base, drafts: { frames: "first edit" } }, versions);
  const key = itemKey(draft); const sent = first.sync.pending[key];
  const second = queueWorkspaceChanges(first, { ...first, drafts: { frames: "newer edit" } }, versions);
  const saved = acknowledgeWorkspaceSave(second, sent, { ...draft, body: "first edit", revision: 5 });
  assert.equal(saved.drafts.frames, "newer edit"); assert.equal(saved.sync.pending[key].body, "newer edit"); assert.equal(saved.sync.pending[key].expectedRevision, 5);
});
test("conflicts preserve both versions and require a concrete user choice", () => {
  const base = mergeRemoteWorkspace(emptyWorkspace(), remote([draft]), "account-a");
  const local = queueWorkspaceChanges(base, { ...base, drafts: { frames: "device edit" } }, versions);
  const conflict = mergeRemoteWorkspace(local, remote([{ ...draft, body: "other device", revision: 5 }]), "account-a");
  const key = itemKey(draft);
  assert.equal(conflict.drafts.frames, "device edit"); assert.equal(conflict.sync.conflicts[key].body, "other device");
  const account = resolveWorkspaceConflict(conflict, key, "account"); assert.equal(account.drafts.frames, "other device"); assert.equal(account.sync.pending[key], undefined);
  const device = resolveWorkspaceConflict(conflict, key, "device"); assert.equal(device.drafts.frames, "device edit"); assert.equal(device.sync.pending[key].expectedRevision, 5);
});
test("same-content replay acknowledges idempotently, and deleted fields send tombstones", () => {
  const base = emptyWorkspace(); base.drafts.frames = "old"; base.bookmarks = ["frames"];
  const cleared = queueWorkspaceChanges(base, { ...base, drafts: {}, bookmarks: [] }, versions);
  assert.equal(cleared.sync.pending["draft:frames@1.0.0"].body, ""); assert.equal(cleared.sync.pending["bookmark:frames@1.0.0"].body, "0");
  const replay = mergeRemoteWorkspace(cleared, remote([{ ...draft, body: "" }]), "account-a");
  assert.equal(replay.sync.pending[itemKey(draft)], undefined);
});
test("retired content text is not hydrated into the current problem", () => {
  const result = mergeRemoteWorkspace(emptyWorkspace(), remote([{ ...draft, slug: "camera", body: "old version" }]), "account-a");
  assert.equal(result.drafts.camera, undefined);
});
test("malformed cache does not break signed-out browsing", () => {
  assert.deepEqual(parseWorkspaceCache("null"), emptyWorkspace());
  assert.deepEqual(parseWorkspaceCache("{broken"), emptyWorkspace());
  assert.deepEqual(parseWorkspaceCache('{"drafts":[1],"submissions":[null]}').drafts, {});
});

test("version changes preserve old work without applying it to a new contract",()=>{
 const old=emptyWorkspace();old.sync.versions={frames:"1.0.0"};old.drafts.frames="old implementation";old.notes.frames="old notes";
 old.sync.pending["bookmark:frames@1.0.0"]={kind:"bookmark",slug:"frames",version:"1.0.0",body:"1",expectedRevision:3};
 const changed=alignWorkspaceVersions(old,{frames:"2.0.0"});
 assert.equal(changed.drafts.frames,undefined);assert.equal(changed.sync.archived["frames@1.0.0"].draft,"old implementation");assert.equal(old.drafts.frames,"old implementation");
 assert.equal(changed.sync.pending["bookmark:frames@2.0.0"].expectedRevision,3);
});
