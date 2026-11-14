"use client";

import { createClient, type SupabaseClient } from "@supabase/supabase-js";

let browserClient: SupabaseClient | null = null;

/** Optional Auth client. Learning records still use the local workspace. */
export function getSupabaseBrowserClient(): SupabaseClient | null {
  if (typeof window === "undefined") return null;
  if (browserClient) return browserClient;

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  )?.trim();
  if (!url || !key) return null;

  // Public keys only. Hosted Auth is allowed over HTTPS; HTTP is loopback-only.
  let endpoint: URL;
  try {
    endpoint = new URL(url);
  } catch {
    return null;
  }
  if (
    !["http:", "https:"].includes(endpoint.protocol) ||
    (endpoint.protocol !== "https:" && !["127.0.0.1", "localhost", "[::1]"].includes(endpoint.hostname)) ||
    endpoint.username ||
    endpoint.password
  ) return null;
  if (key.startsWith("sb_secret_")) return null;

  browserClient = createClient(url, key, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true,
      flowType: "pkce",
    },
  });
  return browserClient;
}
