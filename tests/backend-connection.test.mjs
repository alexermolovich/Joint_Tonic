import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import ts from "typescript";

function load(env = {}) {
  const exports = {};
  class WorkspaceAuthError extends Error { constructor(message, status) { super(message); this.status = status; } }
  const source = ts.transpileModule(fs.readFileSync("apps/web/src/lib/backend-connection.ts", "utf8"), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 },
  }).outputText;
  vm.runInNewContext(source, { exports, URL, Buffer, process: { env }, require(name) {
    assert.equal(name, "./supabase-server");
    return { WorkspaceAuthError, async authenticateRequest(request) {
      if (request.headers.get("authorization") !== "Bearer valid-session") throw new WorkspaceAuthError("Sign in", 401);
      return { user: { id: "verified-owner" } };
    } };
  } });
  return exports;
}

test("signed-out local development preserves workspace ownership only", async () => {
  const api = load();
  const result = await api.backendConnection(new Request("http://localhost:3000", {
    headers: { "x-workspace-id": "local-owner", "x-account-id": "forged-owner" },
  }), "worker");
  assert.equal(result.headers["X-Workspace-Id"], "local-owner");
  assert.equal(result.headers["X-Account-Id"], undefined);
  assert.equal(result.headers.Authorization, undefined);
  assert.equal(result.endpoint.href, "http://127.0.0.1:8765/");
});
test("account requests use verified identity instead of browser ownership headers", async () => {
  const api = load();
  const result = await api.backendConnection(new Request("http://localhost:3000", {
    headers: { authorization: "Bearer valid-session", "x-workspace-id": "someone-else" },
  }), "worker");
  assert.equal(result.headers["X-Workspace-Id"], "verified-owner");
});
test("remote backend requires session and separate service credential", async () => {
  const env = { WORKER_URL: "https://runner.example", WORKER_SERVICE_TOKEN: "a".repeat(32) };
  const api = load(env);
  await assert.rejects(api.backendConnection(new Request("https://web.example"), "worker"), e => e.status === 401);
  const request = new Request("https://web.example", { headers: { authorization: "Bearer valid-session" } });
  const result = await api.backendConnection(request, "worker");
  assert.equal(result.headers.Authorization, `Bearer ${env.WORKER_SERVICE_TOKEN}`);
  assert.equal(result.headers["X-Account-Id"], "verified-owner");
  await assert.rejects(load({ WORKER_URL: env.WORKER_URL }).backendConnection(request, "worker"), e => e.status === 503);
});
test("hosted configuration never falls back to loopback development worker", async () => {
  const api = load({ VERCEL: "1", WORKER_SERVICE_TOKEN: "a".repeat(32) });
  await assert.rejects(api.backendConnection(new Request("https://web.example", {
    headers: { authorization: "Bearer valid-session" },
  }), "worker"), e => e.status === 503);
});
test("credential-bearing and insecure backend URLs are rejected", async () => {
  for (const endpoint of ["http://remote.example", "https://user:pass@remote.example", "https://remote.example/path", "https://remote.example?token=x"]) {
    await assert.rejects(load({ WORKER_URL: endpoint }).backendConnection(new Request("https://web.example"), "worker"), e => e.status === 503);
  }
});
test("request body budget counts UTF-8 bytes", async () => {
  const api = load();
  assert.equal(await api.boundedBody(new Request("http://local", { method: "POST", body: "robot" }), 5), "robot");
  await assert.rejects(api.boundedBody(new Request("http://local", { method: "POST", body: "🤖🤖" }), 5), e => e.status === 413);
});
