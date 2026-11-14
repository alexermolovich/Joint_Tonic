"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "@supabase/supabase-js";
import { getSupabaseBrowserClient } from "@/lib/supabase";

type AuthState = { user: User | null; ready: boolean; configured: boolean; error: string };
const AuthContext = createContext<AuthState>({ user: null, ready: false, configured: false, error: "" });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({ user: null, ready: false, configured: false, error: "" });
  useEffect(() => {
    const client = getSupabaseBrowserClient();
    if (!client) { setState({ user: null, ready: true, configured: false, error: "" }); return; }
    let active = true;
    let revision = 0;
    // Keep callbacks synchronous: awaiting another Auth call here can deadlock its lock.
    const { data: { subscription } } = client.auth.onAuthStateChange((_event, session) => {
      revision++;
      if (active) setState({ user: session?.user ?? null, ready: true, configured: true, error: "" });
    });
    const initialRevision = revision;
    void client.auth.initialize().then(async ({ error }) => {
      if (error) throw error;
      const { data, error: sessionError } = await client.auth.getSession();
      if (sessionError) throw sessionError;
      if (active && revision === initialRevision) setState({ user: data.session?.user ?? null, ready: true, configured: true, error: "" });
    }).catch(() => {
      if (active) setState({ user: null, ready: true, configured: true, error: "Could not restore your session. Try signing in again, or request a fresh email link." });
    });
    return () => { active = false; subscription.unsubscribe(); };
  }, []);
  return <AuthContext.Provider value={state}>{children}</AuthContext.Provider>;
}

export function useAuth() { return useContext(AuthContext); }
