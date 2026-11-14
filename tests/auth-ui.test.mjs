import test from "node:test";
import assert from "node:assert/strict";
import { chromium } from "@playwright/test";

test("signup without confirmation opens the account immediately", { timeout: 60000 }, async () => {
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  try {
    const page = await browser.newPage();
    await page.route("**/auth/v1/**", async route => {
      assert.ok(new URL(route.request().url()).pathname.endsWith("/signup"));
      const user = { id: "33333333-3333-4333-8333-333333333333", email: "instant@example.test", user_metadata: { display_name: "Instant learner" }, app_metadata: {}, aud: "authenticated", created_at: "2026-01-01T00:00:00Z" };
      const access_token = [{ alg: "HS256" }, { sub: user.id, exp: Math.floor(Date.now()/1000)+3600 }, "test"].map(value => Buffer.from(JSON.stringify(value)).toString("base64url")).join(".");
      await route.fulfill({ json: { user, access_token, refresh_token: "test-instant-refresh", expires_in: 3600, token_type: "bearer" } });
    });
    await page.goto("http://localhost:3000/account");
    await page.getByRole("button", { name: "Create an account", exact: true }).click();
    await page.getByLabel("Display name").fill("Instant learner");
    await page.getByLabel("Email", { exact: true }).fill("instant@example.test");
    await page.getByLabel("Password", { exact: true }).fill("test-password");
    await page.getByRole("button", { name: "Create account", exact: true }).click();
    await page.getByRole("heading", { name: "Your account", exact: true }).waitFor();
    assert.equal(await page.getByText("Check your email", { exact: false }).count(), 0);
    await page.reload();
    await page.getByRole("heading", { name: "Your account", exact: true }).waitFor();
    assert.equal(await page.getByLabel("Display name").inputValue(), "Instant learner");
  } finally { await browser.close(); }
});

// Isolated browser contexts and mocked Auth responses; never send real credentials/email.
test("account sign-in, persisted session, profile, password and sign-out", { timeout: 90000 }, async () => {
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on("pageerror", error => errors.push(error.message));
    const user = { id: "11111111-1111-4111-8111-111111111111", aud: "authenticated", role: "authenticated", email: "learner@example.test", app_metadata: { provider: "email" }, user_metadata: { display_name: "Learner" }, created_at: "2026-01-01T00:00:00Z" };
    let rejectLogin = true;
    let profileWrites = 0;
    let passwordWrites = 0;
    const token = () => [ { alg: "HS256", typ: "JWT" }, { sub: user.id, exp: Math.floor(Date.now()/1000)+3600 }, "test" ].map(value => Buffer.from(typeof value === "string" ? value : JSON.stringify(value)).toString("base64url")).join(".");
    await page.route("**/auth/v1/**", async route => {
      const request = route.request();
      const path = new URL(request.url()).pathname;
      const body = request.postDataJSON();
      if (path.endsWith("/token")) {
        if (rejectLogin) return route.fulfill({ status: 400, json: { error_code: "invalid_credentials", msg: "Invalid login credentials" } });
        return route.fulfill({ json: { access_token: token(), refresh_token: "test-refresh-token", expires_in: 3600, token_type: "bearer", user } });
      }
      if (path.endsWith("/user")) {
        if (request.method() === "PUT") {
          if (body.data) { user.user_metadata = body.data; profileWrites++; }
          if (body.password) { assert.equal(body.password, "new-test-password"); passwordWrites++; }
        }
        return route.fulfill({ json: user });
      }
      if (path.endsWith("/logout")) return route.fulfill({ status: 204 });
      return route.fulfill({ status: 400, json: { msg: "Unexpected request in test" } });
    });
    await page.goto("http://localhost:3000/account");
    await page.getByRole("heading", { name: "Welcome back" }).waitFor();
    await page.getByLabel("Email", { exact: true }).fill(user.email);
    await page.getByLabel("Password", { exact: true }).fill("test-password");
    await page.getByRole("button", { name: "Sign in", exact: true }).click();
    await page.getByRole("alert").filter({ hasText: "Invalid login credentials" }).waitFor();
    rejectLogin = false;
    await page.getByRole("button", { name: "Sign in", exact: true }).click();
    await page.getByRole("heading", { name: "Your account" }).waitFor();
    await page.getByLabel("Display name").fill("Robotics learner");
    await page.getByRole("button", { name: "Save account name" }).click();
    await page.getByRole("status").filter({ hasText: "Account name saved" }).waitFor();
    assert.equal(profileWrites, 1);
    await page.reload();
    await page.getByRole("heading", { name: "Your account" }).waitFor();
    assert.equal(await page.getByLabel("Display name").inputValue(), "Robotics learner");
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), "no mobile horizontal overflow");
    await page.getByRole("link", { name: "Change password", exact: true }).click();
    await page.getByLabel("New password", { exact: true }).fill("new-test-password");
    await page.getByRole("button", { name: "Update password", exact: true }).click();
    await page.getByRole("link", { name: "Return to account", exact: true }).click();
    assert.equal(passwordWrites, 1);
    await page.getByRole("button", { name: "Sign out", exact: true }).click();
    await page.getByRole("heading", { name: "Welcome back" }).waitFor();
    await page.reload();
    await page.getByRole("heading", { name: "Welcome back" }).waitFor();
    assert.deepEqual(errors, []);
  } finally { await browser.close(); }
});

test("signup and recovery have fixed local redirects and honest email states", { timeout: 90000 }, async () => {
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  try {
    const page = await browser.newPage();
    const requests = [];
    await page.route("**/auth/v1/**", async route => {
      const url = new URL(route.request().url());
      requests.push({ path: url.pathname, redirect: url.searchParams.get("redirect_to"), body: route.request().postDataJSON() });
      if (url.pathname.endsWith("/signup")) return route.fulfill({ json: { id: "22222222-2222-4222-8222-222222222222", email: "new@example.test", identities: [] } });
      if (url.pathname.endsWith("/recover")) return route.fulfill({ json: {} });
      if (url.pathname.endsWith("/token")) {
        const body = route.request().postDataJSON();
        assert.equal(url.searchParams.get("grant_type"), "pkce");
        assert.equal(body.auth_code, "test-email-code");
        assert.ok(body.code_verifier, "callback includes the verifier from this browser");
        const user = { id: "22222222-2222-4222-8222-222222222222", email: "new@example.test", user_metadata: {}, app_metadata: {}, aud: "authenticated", created_at: "2026-01-01T00:00:00Z" };
        const access_token = [{ alg: "HS256" }, { sub: user.id, exp: Math.floor(Date.now()/1000)+3600 }, "test"].map(value => Buffer.from(JSON.stringify(value)).toString("base64url")).join(".");
        return route.fulfill({ json: { user, access_token, refresh_token: "test-reset-refresh", expires_in: 3600, token_type: "bearer" } });
      }
      return route.fulfill({ status: 400, json: { msg: "Unexpected request in test" } });
    });
    await page.goto("http://localhost:3000/account");
    await page.getByRole("button", { name: "Create an account", exact: true }).click();
    await page.getByLabel("Display name").fill("New learner");
    await page.getByLabel("Email", { exact: true }).fill("new@example.test");
    await page.getByLabel("Password", { exact: true }).fill("test-password");
    await page.getByRole("button", { name: "Create account", exact: true }).click();
    await page.getByRole("status").filter({ hasText: "Check your email" }).waitFor();
    assert.equal(requests[0].redirect, "http://localhost:3000/account");
    assert.ok(requests[0].body.code_challenge, "signup uses PKCE");
    await page.getByRole("button", { name: "Forgot password?", exact: true }).click();
    await page.getByRole("button", { name: "Send reset link", exact: true }).click();
    await page.getByRole("status").filter({ hasText: "If an account matches" }).waitFor();
    assert.equal(requests[1].redirect, "http://localhost:3000/auth/reset-password");
    assert.ok(requests[1].body.code_challenge, "recovery uses PKCE");
    await page.goto("http://localhost:3000/auth/reset-password");
    await page.getByText("Open the password-reset link from your email", { exact: false }).waitFor();
    assert.equal(await page.getByRole("button", { name: "Update password" }).count(), 0);
    await page.goto("http://localhost:3000/auth/reset-password?code=test-email-code");
    await page.getByRole("button", { name: "Update password", exact: true }).waitFor();
    assert.ok(!new URL(page.url()).searchParams.has("code"), "consumed code removed from URL");
  } finally { await browser.close(); }
});
