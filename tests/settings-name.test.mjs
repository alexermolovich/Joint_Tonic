import { after, before, test } from 'node:test';
import { chromium, expect } from '@playwright/test';

// Run against a local web server. Override JOINT_TONIC_TEST_URL for another port
// and JOINT_TONIC_BROWSER_CHANNEL to use an installed browser (for example msedge).
const baseUrl = process.env.JOINT_TONIC_TEST_URL || 'http://127.0.0.1:3000';
const storageKey = 'joint-tonic.workspace.v1';
let browser;

before(async () => {
  browser = await chromium.launch({
    headless: true,
    ...(process.env.JOINT_TONIC_BROWSER_CHANNEL
      ? { channel: process.env.JOINT_TONIC_BROWSER_CHANNEL }
      : {}),
  });
});
after(async () => { await browser?.close(); });

async function openSettings(t) {
  const context = await browser.newContext();
  t.after(() => context.close());
  await context.addInitScript(({ origin, key }) => {
    if (location.origin === origin && !localStorage.getItem(key)) {
      localStorage.setItem(key, JSON.stringify({
        id: 'settings-name-test-workspace', name: 'Saved profile',
        drafts: {}, notes: {}, solved: [], submissions: [], activeJobs: {}, bookmarks: [],
      }));
    }
  }, { origin: new URL(baseUrl).origin, key: storageKey });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/settings`);
  const field = page.getByRole('textbox', { name: 'Display name' });
  await expect(field).toHaveValue('Saved profile');
  return { page, field };
}

async function saveAndReload(page, expected) {
  await page.getByRole('button', { name: 'Save name', exact: true }).click();
  await expect.poll(() => page.evaluate(key => JSON.parse(localStorage.getItem(key)).name, storageKey)).toBe(expected);
  await page.reload();
  await expect(page.getByRole('textbox', { name: 'Display name' })).toHaveValue(expected);
}

test('saving an untouched profile preserves its name after reload', async t => {
  const { page } = await openSettings(t);
  await saveAndReload(page, 'Saved profile');
});

test('saving an edited profile persists the trimmed name after reload', async t => {
  const { page, field } = await openSettings(t);
  await field.fill('  Revised profile  ');
  await saveAndReload(page, 'Revised profile');
});

test('deliberately clearing the profile name persists an empty name', async t => {
  const { page, field } = await openSettings(t);
  await field.fill('');
  await saveAndReload(page, '');
});
