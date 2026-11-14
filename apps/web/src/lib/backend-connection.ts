import { authenticateRequest, WorkspaceAuthError } from "./supabase-server";

export { WorkspaceAuthError };
const loopback = new Set(["127.0.0.1", "localhost", "[::1]"]);

/** Destinations and service credentials come only from server configuration. */
export async function backendConnection(request: Request, kind: "worker" | "simulator") {
  const endpoint = new URL((kind === "worker" ? process.env.WORKER_URL : process.env.SIMULATOR_URL)
    || (kind === "worker" ? "http://127.0.0.1:8765" : "http://127.0.0.1:8766"));
  const local = endpoint.protocol === "http:" && loopback.has(endpoint.hostname);
  if (endpoint.username || endpoint.password || endpoint.search || endpoint.hash || endpoint.pathname !== "/"
    || (!local && endpoint.protocol !== "https:")) throw new WorkspaceAuthError("Backend URL is not configured correctly.", 503);
  const hosted = !!process.env.VERCEL || !local;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (hosted || request.headers.has("authorization")) {
    const { user } = await authenticateRequest(request);
    headers["X-Workspace-Id"] = user.id;
    headers["X-Account-Id"] = user.id;
  } else headers["X-Workspace-Id"] = request.headers.get("x-workspace-id") || "";
  if (hosted) {
    const token = (kind === "worker" ? process.env.WORKER_SERVICE_TOKEN : process.env.SIMULATOR_SERVICE_TOKEN)?.trim();
    if (local || !token || token.length < 32) throw new WorkspaceAuthError("This backend has not been deployed yet.", 503);
    headers.Authorization = `Bearer ${token}`;
  }
  return { endpoint, headers, hosted };
}

export async function boundedBody(request: Request, maximum: number): Promise<string> {
  const reader = request.body?.getReader();
  if (!reader) throw new WorkspaceAuthError("Missing request body.", 400);
  let size = 0;
  const chunks: Uint8Array[] = [];
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > maximum) {
      await reader.cancel();
      throw new WorkspaceAuthError("Request body is too large.", 413);
    }
    chunks.push(value);
  }
  return Buffer.concat(chunks).toString("utf8");
}
