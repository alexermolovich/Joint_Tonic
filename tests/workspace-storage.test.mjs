import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";

test("quota exhaustion retains the latest edit and result in an isolated account cache", () => {
  const modules = new Map(); let snapshot; let fail = true;
  const persisted = new Map();
  const context = {
    structuredClone, AbortController, AbortSignal, Event,
    crypto: { randomUUID: () => "workspace-id" },
    setTimeout: () => 1, clearTimeout() {},
    window: { dispatchEvent() {}, addEventListener() {}, removeEventListener() {} },
    localStorage: {
      getItem: key => persisted.get(key) ?? null,
      setItem(key, value) { if (fail) throw new DOMException("full", "QuotaExceededError"); persisted.set(key,value); },
    },
  };
  function load(name) {
    if (name === "react") return { useState: init => [init(), value => { snapshot = value; }], useEffect: effect => effect() };
    if (name === "./supabase") return { getSupabaseBrowserClient: () => null };
    const base = name.replace(/^\.\//, "").replace(/\.ts$/, "");
    if (modules.has(base)) return modules.get(base);
    const exports = {}; modules.set(base,exports);
    const source = ts.transpileModule(fs.readFileSync(`apps/web/src/lib/${base}.ts`,"utf8"),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText;
    vm.runInNewContext(source,{...context,exports,require:load}); return exports;
  }
  const api = load("local-workspace");
  api.setWorkspaceScope(null,{frames:"1.0.0"});
  api.updateWorkspace(state => ({...state,drafts:{frames:"latest edit"},solved:["frames"],submissions:[{id:"done",slug:"frames",status:"completed"}]}));
  assert.equal(api.readWorkspace().drafts.frames,"latest edit");
  assert.equal(api.readWorkspace().solved[0],"frames");
  assert.equal(api.readWorkspace().submissions[0].id,"done");
  api.useWorkspace(); assert.match(snapshot.message,/Not saved to this device/);
  api.setWorkspaceScope("account-a",{frames:"1.0.0"}); assert.equal(api.readWorkspace().drafts.frames,undefined);
  api.setWorkspaceScope("account-b",{frames:"1.0.0"}); assert.equal(api.readWorkspace().submissions.length,0);
  api.setWorkspaceScope(null,{frames:"1.0.0"}); assert.equal(api.readWorkspace().drafts.frames,"latest edit");
  fail=false; api.updateWorkspace(state=>({...state,notes:{frames:"recovered"}}));
  assert.equal(JSON.parse(persisted.get("joint-tonic.workspace.v1")).drafts.frames,"latest edit");
  api.useWorkspace(); assert.equal(snapshot.status,"local"); assert.equal(snapshot.message,"");
});
