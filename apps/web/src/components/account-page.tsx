"use client";

import Link from "next/link";
import { useEffect, useState, type FormEvent } from "react";
import { useAuth } from "./auth-provider";
import { getSupabaseBrowserClient } from "@/lib/supabase";
import "./account-page.css";

type Mode = "signin" | "signup" | "recover";

export function AccountPage({ resetPassword = false }: { resetPassword?: boolean }) {
  const { user, ready, configured, error: sessionError } = useAuth();
  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [passwordUpdated, setPasswordUpdated] = useState(false);
  useEffect(() => { setName(typeof user?.user_metadata.display_name === "string" ? user.user_metadata.display_name : ""); }, [user?.id, user?.user_metadata.display_name]);

  async function act(action: () => Promise<void>) {
    if (busy) return;
    setBusy(true); setError(""); setMessage("");
    try { await action(); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Could not reach Supabase. Please try again."); }
    finally { setBusy(false); }
  }
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const client = getSupabaseBrowserClient();
    if (!client) return;
    void act(async () => {
      if (resetPassword && user) {
        const { error } = await client.auth.updateUser({ password });
        if (error) throw error;
        setPassword(""); setPasswordUpdated(true); setMessage("Password updated. You can return to your account.");
      } else if (user) {
        const { error } = await client.auth.updateUser({ data: { display_name: name.trim() } });
        if (error) throw error;
        setMessage("Account name saved.");
      } else if (mode === "signup") {
        const { data, error } = await client.auth.signUp({ email: email.trim(), password, options: { data: { display_name: name.trim() }, emailRedirectTo: `${window.location.origin}/account` } });
        if (error) throw error;
        setPassword(""); setMessage(data.session ? "Your account is ready." : "Check your email to confirm your account. Open the link in this browser. If you already have an account, sign in or reset your password.");
      } else if (mode === "recover") {
        const { error } = await client.auth.resetPasswordForEmail(email.trim(), { redirectTo: `${window.location.origin}/auth/reset-password` });
        if (error) throw error;
        setMessage("If an account matches this email, you’ll receive a reset link. Open it in this browser.");
      } else {
        const { error } = await client.auth.signInWithPassword({ email: email.trim(), password });
        if (error) throw error;
        setPassword("");
      }
    });
  }

  const title = resetPassword ? "Reset your password" : user ? "Your account" : mode === "signup" ? "Create your account" : mode === "recover" ? "Forgot your password?" : "Welcome back";
  return <main id="main" className="page detail-page jt-auth-page">
    <span className="eyebrow">JOINT TONIC ACCOUNT</span><h1>{title}</h1>
    {!ready ? <p role="status">Loading your account…</p> : !configured ? <section className="settings-card"><h2>Sign-in isn’t configured yet</h2><p>Add the Supabase URL and publishable key to the local web environment, then restart the web server.</p><Link className="button secondary" href="/problems">Browse problems</Link></section> : <section className="settings-card jt-auth-card">
      {sessionError && <p role="alert" className="test-fail">{sessionError}</p>}
      {error && <p role="alert" className="test-fail">{error}</p>}
      {message && <p role="status">{message}</p>}
      {resetPassword && !user ? <><p>Open the password-reset link from your email in the same browser where you requested it.</p><Link href="/account" className="text-link">Return to sign-in</Link></> : passwordUpdated ? <Link href="/account" className="button primary">Return to account</Link> : <>
        {user && <p>Signed in as <strong>{user.email}</strong></p>}
        <form onSubmit={submit} aria-busy={busy}>
          <fieldset disabled={busy}>
            {!resetPassword && (user || mode === "signup") && <label>Display name<input className="text-input" value={name} maxLength={80} autoComplete="nickname" onChange={event => setName(event.target.value)} /></label>}
            {!user && <label>Email<input className="text-input" type="email" required autoComplete="email" value={email} onChange={event => setEmail(event.target.value)} /></label>}
            {(resetPassword || (!user && mode !== "recover")) && <><label>{resetPassword ? "New password" : "Password"}<input className="text-input" type="password" required minLength={mode === "signup" || resetPassword ? 8 : undefined} maxLength={128} aria-describedby={mode === "signup" || resetPassword ? "password-guidance" : undefined} autoComplete={mode === "signup" || resetPassword ? "new-password" : "current-password"} value={password} onChange={event => setPassword(event.target.value)} /></label>{(mode === "signup" || resetPassword) && <small id="password-guidance">Use at least 8 characters.</small>}</>}
            <button className="button primary" type="submit">{busy ? "Please wait…" : resetPassword ? "Update password" : user ? "Save account name" : mode === "signup" ? "Create account" : mode === "recover" ? "Send reset link" : "Sign in"}</button>
          </fieldset>
        </form>
        {!user && <div className="jt-auth-actions">{(["signin", "signup", "recover"] as Mode[]).filter(item => item !== mode).map(item => <button type="button" className="text-link" disabled={busy} key={item} onClick={() => { setMode(item); setError(""); setMessage(""); setPassword(""); }}>{item === "signin" ? "Sign in" : item === "signup" ? "Create an account" : "Forgot password?"}</button>)}</div>}
        {user && <div className="jt-auth-actions"><Link className="text-link" href="/auth/reset-password">Change password</Link><button type="button" className="button secondary" disabled={busy} onClick={() => { void act(async () => { const { error } = await getSupabaseBrowserClient()!.auth.signOut({ scope: "local" }); if (error) throw error; setPassword(""); setMessage("Signed out on this device."); }); }}>Sign out</button></div>}
      </>}
    </section>}
    <p className="jt-auth-note">Your account has a separate saved workspace. Drafts, notes and bookmarks sync when connected; verified submissions and progress come from the evaluation service. Signed-out browser work is never imported automatically.</p>
    <Link className="text-link" href="/progress">View this device’s progress</Link>
  </main>;
}
