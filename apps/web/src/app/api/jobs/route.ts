import { NextRequest, NextResponse } from "next/server";
import { backendConnection, boundedBody, WorkspaceAuthError } from "@/lib/backend-connection";

export async function POST(request: NextRequest) {
  const correlationId = crypto.randomUUID();
  const respond = (body: unknown, status: number) => NextResponse.json(body, {
    status, headers: { "x-correlation-id": correlationId, "Cache-Control": "no-store" },
  });
  const origin = request.headers.get("origin");
  if (origin && origin !== request.nextUrl.origin) return respond({ error: "Cross-origin request rejected" }, 403);
  try {
    const body = await boundedBody(request, 100000);
    const connection = await backendConnection(request, "worker");
    const response = await fetch(new URL("/jobs", connection.endpoint), {
      method: "POST", headers: { ...connection.headers, "x-correlation-id": correlationId },
      body, signal: AbortSignal.timeout(5000), cache: "no-store",
    });
    console.info(JSON.stringify({ event: "evaluation.request", correlation_id: correlationId, status: response.status }));
    return respond(await response.json(), response.status);
  } catch (error) {
    if (error instanceof WorkspaceAuthError) return respond({ error: error.message }, error.status);
    console.warn(JSON.stringify({ event: "evaluation.unavailable", correlation_id: correlationId }));
    return respond({ error: process.env.VERCEL ? "Code execution is not available on this deployment yet. Your editor remains available."
      : "The isolated runner is offline. Start npm run dev to launch the local worker." }, 503);
  }
}
