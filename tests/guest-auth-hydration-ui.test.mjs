import test from "node:test";
import { chromium, expect } from "@playwright/test";

test("guest Simulation selection survives delayed Auth initialization", { timeout: 60000 }, async () => {
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  try {
    const page = await browser.newPage();
    await page.addInitScript(() => {
      const request = navigator.locks.request.bind(navigator.locks);
      let release;
      const gate = new Promise(resolve => { release = resolve; });
      window.releaseTestAuth = release;
      navigator.locks.request = async (name, ...args) => {
        if (name.includes("auth-token")) { window.testAuthBlocked = true; await gate; }
        return request(name, ...args);
      };
    });
    await page.route("**/api/simulator/fr3", route => route.fulfill({ status: 503, json: {
      code: "simulator_not_deployed", error: "Online simulation is not deployed.",
    } }));
    await page.goto(`${process.env.APP_BASE_URL || "http://localhost:3000"}/problems/fr3-joint-interpolation`);
    await page.waitForFunction(() => window.testAuthBlocked === true);
    const simulation = page.getByRole("tab", { name: "Simulation", exact: true });
    await simulation.click();
    await expect(simulation).toHaveAttribute("aria-selected", "true");
    await page.evaluate(() => window.releaseTestAuth());
    // The guest cache is written when identity restoration completes.
    await page.waitForFunction(() => localStorage.getItem("joint-tonic.workspace.v1") !== null);
    await expect(page.getByText("Saved on this device", { exact: true })).toBeVisible();
    await expect(simulation).toHaveAttribute("aria-selected", "true");
    await expect(page.getByRole("link", { name: "Open the local Franka demo", exact: true })).toBeVisible();
  } finally { await browser.close(); }
});
