import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";

function load({ verified = true, configured = true } = {}) {
  const calls = []; const exports = {};
  const source = ts.transpileModule(fs.readFileSync("apps/web/src/lib/supabase-server.ts", "utf8"), { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 } }).outputText;
  vm.runInNewContext(source, { exports, URL, process: { env: configured ? { NEXT_PUBLIC_SUPABASE_URL: "https://example.supabase.co", NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: "sb_publishable_test" } : {} }, require(name) {
    assert.equal(name, "@supabase/supabase-js"); return { createClient(url, key, options) { calls.push({ url, key, options }); return { auth: { async getUser(token) { calls.push({ token }); return verified ? { data: { user: { id: "server-verified-owner" } }, error: null } : { data: { user: null }, error: new Error("invalid") }; } } }; } };
  } });
  return { ...exports, calls };
}
test("workspace UUID or arbitrary JWT payload never establishes identity", async () => {
  const api = load();
  await assert.rejects(api.authenticateRequest(new Request("https://joint.test/api/workspace", { headers: { "x-workspace-id": "victim" } })), e => e.status === 401);
  assert.equal(api.calls.length, 0);
  const rejected = load({ verified: false });
  await assert.rejects(rejected.authenticateRequest(new Request("https://joint.test", { headers: { Authorization: "Bearer forged.token.value" } })), e => e.status === 401);
});
test("verified bearer identity and RLS client token are the same session", async () => {
  const api = load(); const result = await api.authenticateRequest(new Request("https://joint.test", { headers: { Authorization: "Bearer test-token" } }));
  assert.equal(result.user.id, "server-verified-owner"); assert.equal(result.accessToken, "test-token");
  assert.equal(api.calls[0].options.global.headers.Authorization, "Bearer test-token"); assert.equal(api.calls[1].token, "test-token");
});
test("missing configuration fails closed", async () => {
  const api = load({ configured: false });
  await assert.rejects(api.authenticateRequest(new Request("https://joint.test", { headers: { Authorization: "Bearer test-token" } })), e => e.status === 503);
});
