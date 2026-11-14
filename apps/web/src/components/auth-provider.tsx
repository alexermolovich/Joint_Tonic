"use client";

import { createContext, Fragment, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "@supabase/supabase-js";
import { getSupabaseBrowserClient } from "@/lib/supabase";
import { setWorkspaceScope } from "@/lib/local-workspace";
import { WorkspaceSyncEvents } from "./workspace-sync";

type AuthState = { user: User | null; ready: boolean; configured: boolean; error: string };
const AuthContext = createContext<AuthState>({ user: null, ready: false, configured: false, error: "" });

export function AuthProvider({ children, problemVersions }: { children: ReactNode; problemVersions: Record<string,string> }) {
  const [state, setState] = useState<AuthState>({ user: null, ready: false, configured: false, error: "" });
  useEffect(() => {
    const publish = (next: AuthState) => { setWorkspaceScope(next.user?.id ?? null, problemVersions); setState(next); };
    const client = getSupabaseBrowserClient();
    if (!client) { publish({ user: null, ready: true, configured: false, error: "" }); return; }
    let active = true;
    let revision = 0;
    // Keep callbacks synchronous: awaiting another Auth call here can deadlock its lock.
    const { data: { subscription } } = client.auth.onAuthStateChange((_event, session) => {
      revision++;
      if (active) publish({ user: session?.user ?? null, ready: true, configured: true, error: "" });
    });
    const initialRevision = revision;
    void client.auth.initialize().then(async ({ error }) => {
      if (error) throw error;
      const { data, error: sessionError } = await client.auth.getSession();
      if (sessionError) throw sessionError;
      if (active && revision === initialRevision) publish({ user: data.session?.user ?? null, ready: true, configured: true, error: "" });
    }).catch(() => {
      if (active && revision === initialRevision) publish({ user: null, ready: true, configured: true, error: "Could not restore your session. Try signing in again, or request a fresh email link." });
    });
    return () => { active = false; subscription.unsubscribe(); };
  }, [problemVersions]);
  // Pending identity has no private workspace. Keep guest UI mounted when Auth
  // confirms no session; actual account changes still remount to isolate drafts.
  return <AuthContext.Provider value={state}><WorkspaceSyncEvents/><Fragment key={state.user?.id ?? "guest"}>{children}</Fragment></AuthContext.Provider>;
}

export function useAuth() { return useContext(AuthContext); }
