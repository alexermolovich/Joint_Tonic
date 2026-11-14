import { timingSafeEqual } from "node:crypto";
import { createClient } from "@supabase/supabase-js";
import { NextRequest, NextResponse } from "next/server";
import { boundedBody, WorkspaceAuthError } from "@/lib/backend-connection";

/** Trusted-worker callback. Browser sessions cannot create evaluation evidence. */
export async function POST(request: NextRequest) {
  const correlationId = crypto.randomUUID();
  const respond = (body: unknown, status: number) => NextResponse.json(body, {
    status, headers: { "Cache-Control": "no-store", "x-correlation-id": correlationId },
  });
  const secret = process.env.WORKER_SERVICE_TOKEN?.trim();
  const received = request.headers.get("authorization") || "";
  const expected = `Bearer ${secret || ""}`;
  if (!secret || secret.length < 32 || Buffer.byteLength(received) !== Buffer.byteLength(expected)
      || !timingSafeEqual(Buffer.from(received), Buffer.from(expected))) return respond({ error: "Trusted worker authentication required" }, 401);
  try {
    const envelope = JSON.parse(await boundedBody(request, 524288));
    if (!envelope || typeof envelope !== "object" || Array.isArray(envelope) || Object.keys(envelope).length !== 1 || !envelope.p_job) return respond({ error: "Invalid evaluation envelope" }, 400);
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const key = process.env.SUPABASE_SECRET_KEY;
    if (!url || !key) return respond({ error: "Verified history storage is not configured" }, 503);
    const endpoint = new URL(url);
    if (endpoint.protocol !== "https:" && !(endpoint.protocol === "http:" && ["localhost", "127.0.0.1", "[::1]"].includes(endpoint.hostname))) return respond({ error: "Invalid history storage configuration" }, 503);
    if (endpoint.username || endpoint.password) return respond({ error: "Invalid history storage configuration" }, 503);
    const client = createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false } });
    const { data, error } = await client.rpc("record_evaluation", { p_job: envelope.p_job });
    if (error) {
      console.warn(JSON.stringify({ event: "evaluation.persistence_rejected", correlation_id: correlationId, code: error.code }));
      return respond({ error: "Evaluation could not be persisted. Check catalog lineage and migrations." }, 409);
    }
    console.info(JSON.stringify({ event: "evaluation.persisted", correlation_id: correlationId, job_id: data?.id }));
    return respond(data, 200);
  } catch (error) {
    if (error instanceof WorkspaceAuthError) return respond({ error: error.message }, error.status);
    if (error instanceof SyntaxError) return respond({ error: "Invalid evaluation JSON" }, 400);
    return respond({ error: "Evaluation storage temporarily unavailable" }, 503);
  }
}
