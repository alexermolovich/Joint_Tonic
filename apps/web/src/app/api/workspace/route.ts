import { NextResponse } from "next/server";
import { randomUUID } from "node:crypto";
import { authenticateRequest, WorkspaceAuthError } from "@/lib/supabase-server";
import { getProblems } from "@/lib/content";
import { parseWorkspaceChange, type WorkspaceItem } from "@/lib/workspace-protocol";
import { boundedBody } from "@/lib/backend-connection";

export const dynamic = "force-dynamic";
function reply(value: unknown, status = 200, correlation: string = randomUUID()) { return NextResponse.json(value, { status, headers: { "Cache-Control": "private, no-store", "X-Correlation-Id": correlation } }); }
function failure(error: unknown, correlation: string) {
  const status = error instanceof WorkspaceAuthError ? error.status : 503;
  console.warn(JSON.stringify({ event: "workspace_request_failed", correlation_id: correlation, status }));
  return reply({ error: error instanceof WorkspaceAuthError ? error.message : "Account storage is unavailable. Your pending edits remain on this device.", correlationId: correlation }, status, correlation);
}

export async function GET(request: Request) {
  const correlation = randomUUID();
  try {
    const { user, client } = await authenticateRequest(request);
    const queries = await Promise.all([
      client.from("problem_versions").select("id,version,problems!inner(slug)").not("published_at", "is", null),
      client.from("drafts").select("problem_version_id,code,revision").eq("user_id", user.id),
      client.from("notes").select("problem_version_id,body,revision").eq("user_id", user.id),
      client.from("bookmarks").select("problem_id,bookmarked,revision,problems!inner(slug)").eq("user_id", user.id),
      client.from("progress").select("problem_version_id").eq("user_id", user.id),
      client.from("jobs").select("id,problem_version_id,mode,status,code,created_at,result,error").eq("user_id", user.id).eq("mode", "submit").order("created_at", { ascending: false }).limit(100),
      client.from("jobs").select("id,problem_version_id,status,created_at").eq("user_id", user.id).in("status", ["queued", "running"]).order("created_at", { ascending: false }).limit(100),
    ]);
    if (queries.some(q => q.error)) throw new Error("workspace read failed");
    const versions = Object.fromEntries(getProblems().map(p => [p.slug, p.version]));
    const versionRows = new Map((queries[0].data || []).map(v => [v.id, { slug: (v.problems as unknown as { slug: string }).slug, version: v.version }]));
    const items: WorkspaceItem[] = [];
    for (const [index, kind] of [[1, "draft"], [2, "note"]] as const) for (const row of queries[index].data || []) {
      const r = row as unknown as { problem_version_id: string; code?: string; body?: string; revision: number };
      const version = versionRows.get(r.problem_version_id);
      if (version) items.push({ ...version, kind, body: r.code ?? r.body ?? "", revision: r.revision });
    }
    for (const row of queries[3].data || []) {
      const r = row as unknown as { bookmarked: boolean; revision: number; problems: { slug: string } };
      const slug = r.problems.slug;
      if (versions[slug]) items.push({ kind: "bookmark", slug, version: versions[slug], body: r.bookmarked ? "1" : "0", revision: r.revision });
    }
    const solved = (queries[4].data || []).flatMap(row => { const v = versionRows.get((row as unknown as { problem_version_id: string }).problem_version_id); return v && versions[v.slug] === v.version ? [v.slug] : []; });
    const submissions = (queries[5].data || []).flatMap(row => {
      const r = row as unknown as { id: string; problem_version_id: string; mode: string; status: string; code: string; created_at: string; result: Record<string, unknown> | null; error: string | null };
      const v = versionRows.get(r.problem_version_id);
      return v ? [{ ...(r.result || {}), id: r.id, slug: v.slug, mode: r.mode, status: r.status === "cancelled" ? "failed" : r.status, code: r.code, created_at: r.created_at, ...(r.error ? { error: r.error } : {}) }] : [];
    });
    const activeJobs: Record<string, string> = {};
    for (const row of queries[6].data || []) { const r = row as unknown as { id: string; problem_version_id: string }; const v = versionRows.get(r.problem_version_id); if (v && !activeJobs[v.slug]) activeJobs[v.slug] = r.id; }
    console.info(JSON.stringify({ event: "workspace_read", correlation_id: correlation, item_count: items.length, history_count: submissions.length }));
    return reply({ ownerId: user.id, items, versions, solved, submissions, activeJobs }, 200, correlation);
  } catch (error) { return failure(error, correlation); }
}

export async function PATCH(request: Request) {
  const correlation = randomUUID();
  try {
    const origin = request.headers.get("origin");
    if (origin && new URL(origin).origin !== new URL(request.url).origin) return reply({ error: "Cross-origin request rejected." }, 403, correlation);
    const { client } = await authenticateRequest(request);
    const text = await boundedBody(request, 610000);
    let change;
    try { change = parseWorkspaceChange(JSON.parse(text)); } catch { return reply({ error: "Invalid workspace change." }, 400, correlation); }
    if (!getProblems().some(p => p.slug === change.slug && p.version === change.version)) return reply({ error: "This content version is no longer editable. Your local text is preserved." }, 409, correlation);
    const version = await client.from("problem_versions").select("id,problems!inner(slug)").eq("problems.slug", change.slug).eq("version", change.version).not("published_at", "is", null).single();
    if (version.error || !version.data) throw new Error("content not provisioned");
    const saved = await client.rpc("save_workspace_item", { p_problem_version_id: version.data.id, p_kind: change.kind, p_body: change.body, p_expected_revision: change.expectedRevision });
    if (saved.error) throw new Error("workspace save failed");
    const result = saved.data as { ok: boolean; revision: number; body: string };
    console.info(JSON.stringify({ event: result.ok ? "workspace_saved" : "workspace_conflict", correlation_id: correlation, kind: change.kind, problem_slug: change.slug }));
    return reply({ ...result, kind: change.kind, slug: change.slug, version: change.version }, result.ok ? 200 : 409, correlation);
  } catch (error) { return failure(error, correlation); }
}
