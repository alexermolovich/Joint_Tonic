import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";
import * as crypto from "node:crypto";

function load({ configured = true, rejected = false } = {}) {
  const calls = [], exports = {};
  const token = "worker-test-token-".repeat(3);
  class WorkspaceAuthError extends Error { constructor(message, status) { super(message); this.status = status; } }
  const source = ts.transpileModule(fs.readFileSync("apps/web/src/app/api/evaluations/route.ts", "utf8"), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 },
  }).outputText;
  vm.runInNewContext(source, { exports, URL, Buffer, crypto, console: { info() {}, warn() {} }, process: { env: configured ? {
    WORKER_SERVICE_TOKEN: token, NEXT_PUBLIC_SUPABASE_URL: "https://example.supabase.co", SUPABASE_SECRET_KEY: "test-server-key",
  } : {} }, require(name) {
    if (name === "node:crypto") return crypto;
    if (name === "next/server") return { NextResponse: { json: (value, options) => Response.json(value, options) } };
    if (name === "@/lib/backend-connection") return { WorkspaceAuthError, boundedBody: request => request.text() };
    if (name === "@supabase/supabase-js") return { createClient() { return { async rpc(name, body) {
      calls.push({ name, body }); return rejected ? { error: { code: "23514" }, data: null } : { error: null, data: { id: body.p_job.id, persisted: true } };
    } }; } };
    throw new Error(name);
  } });
  return { ...exports, calls, token };
}

test("browser sessions and missing configuration cannot submit grading evidence", async () => {
  for (const setup of [{}, { configured: false }]) {
    const api = load(setup);
    const response = await api.POST(new Request("https://web.example/api/evaluations", {
      method: "POST", headers: { authorization: "Bearer ordinary-user-session" }, body: JSON.stringify({ p_job: { passed: true } }),
    }));
    assert.equal(response.status, 401); assert.equal(api.calls.length, 0);
  }
});
test("only worker-authenticated envelopes reach the service-only transaction", async () => {
  const api = load();
  const response = await api.POST(new Request("https://web.example/api/evaluations", {
    method: "POST", headers: { authorization: `Bearer ${api.token}` }, body: JSON.stringify({ p_job: { id: "test-job" } }),
  }));
  assert.equal(response.status, 200); assert.equal(api.calls[0].name, "record_evaluation");
  assert.equal(api.calls[0].body.p_job.id, "test-job"); assert.equal(response.headers.get("cache-control"), "no-store");
});
test("lineage rejection is reported without database details", async () => {
  const api = load({ rejected: true });
  const response = await api.POST(new Request("https://web.example/api/evaluations", {
    method: "POST", headers: { authorization: `Bearer ${api.token}` }, body: JSON.stringify({ p_job: { id: "test-job" } }),
  }));
  assert.equal(response.status, 409);
  assert.equal((await response.text()).includes("test-server-key"), false);
});
