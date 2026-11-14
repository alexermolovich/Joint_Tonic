import { createClient, type SupabaseClient, type User } from "@supabase/supabase-js";

export class WorkspaceAuthError extends Error {
  constructor(message: string, public status: number) { super(message); }
}

/** Validates identity with Auth; a decoded JWT or workspace UUID is not identity. */
export async function authenticateRequest(request: Request): Promise<{ user: User; client: SupabaseClient; accessToken: string }> {
  const header = request.headers.get("authorization") || "";
  if (!/^Bearer [^\s]+$/.test(header) || header.length > 8192) throw new WorkspaceAuthError("Sign in to access saved account data.", 401);
  const accessToken = header.slice(7);
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)?.trim();
  if (!url || !key || key.startsWith("sb_secret_")) throw new WorkspaceAuthError("Account storage is not configured.", 503);
  let endpoint: URL;
  try { endpoint = new URL(url); } catch { throw new WorkspaceAuthError("Account storage is not configured.", 503); }
  if (endpoint.username || endpoint.password || (endpoint.protocol !== "https:" && !(endpoint.protocol === "http:" && ["localhost", "127.0.0.1", "[::1]"].includes(endpoint.hostname)))) throw new WorkspaceAuthError("Account storage is not configured.", 503);
  const client = createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false }, global: { headers: { Authorization: `Bearer ${accessToken}` } } });
  let result;
  try { result = await client.auth.getUser(accessToken); }
  catch { throw new WorkspaceAuthError("Could not verify your session. Try again.", 503); }
  if (result.error || !result.data.user) throw new WorkspaceAuthError("Your session expired. Sign in again.", 401);
  return { user: result.data.user, client, accessToken };
}
