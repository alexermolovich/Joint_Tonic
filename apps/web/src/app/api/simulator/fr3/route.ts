import { NextRequest, NextResponse } from "next/server";
import { backendConnection, WorkspaceAuthError } from "@/lib/backend-connection";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const correlationId = crypto.randomUUID();
  const respond = (body: unknown, status: number) => NextResponse.json(body, { status, headers: { "x-correlation-id": correlationId, "Cache-Control": "no-store" } });
  const origin = request.headers.get("origin");
  if (origin && origin !== request.nextUrl.origin) return respond({ error: "Cross-origin request rejected" }, 403);
  try {
    if (Number(request.headers.get("content-length") || 0) > 2048) return respond({ error: "Pose request too large" }, 413);
    const reader = request.body?.getReader();
    if (!reader) return respond({ error: "Missing pose request" }, 400);
    const chunks: Uint8Array[] = [];
    let length = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > 2048) { await reader.cancel(); return respond({ error: "Pose request too large" }, 413); }
      chunks.push(value);
    }
    const body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    if (!body || typeof body !== "object" || Array.isArray(body) || Object.keys(body).some(key => key !== "q" && key !== "camera")) return respond({ error: "Expected an optional seven-joint pose and camera" }, 400);
    if (body.q !== undefined && (!Array.isArray(body.q) || body.q.length !== 7 || body.q.some((q: unknown) => typeof q !== "number" || !Number.isFinite(q)))) return respond({ error: "Expected seven finite joint angles in radians" }, 400);
    if (body.camera !== undefined) {
      const c = body.camera;
      const bounds: [string, number, number][] = [["azimuth", -360, 360], ["elevation", -85, 85], ["distance", .5, 4]];
      if (!c || typeof c !== "object" || Array.isArray(c) || Object.keys(c).length !== 3 || bounds.some(([key, low, high]) => typeof c[key] !== "number" || !Number.isFinite(c[key]) || c[key] < low || c[key] > high)) return respond({ error: "Invalid orbit camera" }, 400);
    }
    const connection = await backendConnection(request, "simulator");
    const response = await fetch(new URL("/v1/fr3/frame", connection.endpoint), { method: "POST", headers: { ...connection.headers, "x-correlation-id": correlationId }, body: JSON.stringify(body), signal: AbortSignal.timeout(30000), cache: "no-store" });
    const data = await response.json();
    console.info(JSON.stringify({ event: "simulator.frame", correlation_id: correlationId, status: response.status }));
    return respond(data, response.status);
  } catch (error) {
    if (error instanceof WorkspaceAuthError) return respond({ error: error.message }, error.status);
    if (error instanceof SyntaxError) return respond({ error: "Invalid pose JSON" }, 400);
    console.warn(JSON.stringify({ event: "simulator.unavailable", correlation_id: correlationId }));
    return respond({ error: "MuJoCo is unavailable. Start the local simulator using the setup instructions, then retry." }, 503);
  }
}
