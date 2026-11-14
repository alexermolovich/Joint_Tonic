# Supabase login and accounts

The localhost website can now use the user-supplied hosted Supabase Auth project. The evaluator remains local. No remote SQL migrations or privileged keys are needed for this account slice.

## Local configuration

Set these in ignored `apps/web/.env.local`:

```dotenv
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-publishable-key
```

The legacy `NEXT_PUBLIC_SUPABASE_ANON_KEY` remains supported. Only a public/publishable client key belongs here. Never use a secret or service-role key. Rotate any secret shared in chat through the Supabase dashboard; its replacement is not needed by this application. Restart the web server if it has not reloaded environment changes.

## Required project settings

In Supabase **Authentication → URL Configuration**, use `http://localhost:3000` as the development Site URL and add these exact Redirect URLs:

- `http://localhost:3000/account`
- `http://localhost:3000/auth/reset-password`
- `http://127.0.0.1:3000/account`
- `http://127.0.0.1:3000/auth/reset-password`

Enable the Email provider and email/password signup. For the current testing phase, the user has requested signup without email confirmation: in Authentication → Sign In / Providers → Email, turn Confirm email OFF and save. This hosted setting must be changed in the dashboard; the publishable application key cannot change it. The application already accepts the immediate session returned by Supabase without an additional confirmation screen. Custom SMTP is still needed for reliable password-reset delivery; it is no longer a prerequisite for new-account signup when confirmation is disabled. Supabase's default sender has recipient and rate restrictions. If the project requires CAPTCHA or additional authentication factors, those require an additional UI integration; the first slice provides email/password only.

Use one hostname consistently: localhost and 127.0.0.1 have different browser storage. PKCE confirmation/reset links must open in the browser that requested them. A fresh reset request is the recovery path for an expired link or lost verifier. No external return-to URL is accepted by this implementation.

## Account behavior

- `/account`: signup, sign-in, editable display name, session restoration, and device-scoped sign-out.
- `/auth/reset-password`: recovery callback and signed-in password changes.
- Display name persists in Supabase Auth `user_metadata.display_name`. It is display data, not a role or authorization claim. `public.profiles` is not used in this slice, avoiding a dependency on unapplied hosted schema migrations.
- The SDK handles PKCE callbacks, session refresh, and sign-out propagation across tabs.
- Browsing and local coding stay available signed out. Drafts, notes, bookmarks, progress, and job history remain browser-local, shared by users of that browser workspace. Sign-out does not erase those records. Export/reset is in Settings.
- Account auth does not turn local UUID-owned jobs into authenticated cloud submissions. Server-verified identity, content ingestion, RLS-backed private workspace records, and trusted evaluation persistence remain the next adapter stage. Never upload local solved flags as verified progress.

## Verification

Run `npm run typecheck`. With the development server on port 3000, run `node --test tests/auth-ui.test.mjs` for isolated browser tests against mocked Auth responses. These test application behavior without creating real hosted accounts or sending emails.

For the live smoke test after disabling Confirm email, create a new account at `/account` and verify that Your account appears immediately, then reload, change the account name, and sign out/in. Password reset remains a separate email-based recovery flow. Live email delivery and dashboard redirect allowlisting cannot be verified using a publishable key; finish them in the project dashboard. No live test account is created automatically.

Official references: [signup](https://supabase.com/docs/reference/javascript/auth-signup), [password reset](https://supabase.com/docs/reference/javascript/auth-resetpasswordforemail), [redirect URLs](https://supabase.com/docs/guides/auth/redirect-urls), [email delivery](https://supabase.com/docs/guides/auth/auth-smtp).
