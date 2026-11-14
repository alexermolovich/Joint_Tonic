import test from "node:test";
import assert from "node:assert/strict";
import { buildAccountStats } from "../apps/web/src/lib/account-stats.ts";
import type { Job, ProblemMeta } from "../apps/web/src/lib/types.ts";

const problems = [{ slug: "frames", domain: "Geometry" }, { slug: "camera", domain: "Perception" }] as ProblemMeta[];
const local = (year: number, month: number, day: number) => new Date(year, month - 1, day, 12);
const job = (id: string, slug: string, date: Date, passed = true): Job => ({ id, slug, mode: "submit", status: "completed", created_at: date.toISOString(), code: "", passed });

test("empty history has zero counts, no acceptance rate and a complete year", () => {
  const stats = buildAccountStats(problems, { solved: [], submissions: [] }, local(2026, 11, 13));
  assert.equal(stats.solvedSlugs.size, 0); assert.equal(stats.totalSubmissions, 0);
  assert.equal(stats.acceptanceRate, null); assert.equal(stats.currentStreak, 0); assert.equal(stats.bestStreak, 0);
  assert.equal(stats.days.length, 365); assert.deepEqual(stats.recentAccepted, []);
});

test("deduplicates records and solved problems; excludes platform failures from grading", () => {
  const accepted = job("a", "frames", local(2026, 11, 12));
  const repeat = job("b", "frames", local(2026, 11, 13));
  const rejected = job("c", "camera", local(2026, 11, 13), false);
  const platform = { ...job("d", "camera", local(2026, 11, 13)), status: "failed" as const };
  const stats = buildAccountStats(problems, { solved: ["frames", "frames", "removed"], submissions: [repeat, accepted, accepted, rejected, platform] }, local(2026, 11, 13));
  assert.equal(stats.totalSubmissions, 4); assert.equal(stats.gradedSubmissions, 3); assert.equal(stats.acceptanceRate, 67);
  assert.deepEqual([...stats.solvedSlugs], ["frames"]); assert.equal(stats.recentAccepted.length, 1); assert.equal(stats.recentAccepted[0].id, "b");
  assert.equal(stats.domains[0].accepted, 2); assert.equal(stats.domains[1].needsWork, 1); assert.equal(stats.platformFailures, 1);
});

test("current streak can end yesterday; same-day submissions count only one active day", () => {
  const submissions = [job("a", "frames", local(2026, 3, 7)), job("b", "frames", local(2026, 3, 8)), job("c", "camera", local(2026, 3, 8), false), job("d", "camera", local(2026, 3, 9))];
  const stats = buildAccountStats(problems, { solved: [], submissions }, local(2026, 3, 10));
  assert.equal(stats.currentStreak, 3); assert.equal(stats.bestStreak, 3); assert.equal(stats.activeDaysThisYear, 3);
  assert.equal(stats.days.find(day => day.date === "2026-03-08")?.submissions, 2);
  assert.equal(buildAccountStats(problems, { solved: [], submissions }, local(2026, 3, 11)).currentStreak, 0);
});

test("streak crosses year boundary and ignores invalid/future dates in the calendar", () => {
  const submissions = [job("a", "frames", local(2025, 12, 31)), job("b", "camera", local(2026, 1, 1)), job("c", "frames", local(2027, 1, 1)), { ...job("d", "frames", local(2026, 1, 1)), created_at: "invalid" }];
  const stats = buildAccountStats(problems, { solved: [], submissions }, local(2026, 1, 1));
  assert.equal(stats.currentStreak, 2); assert.equal(stats.bestStreak, 2); assert.equal(stats.submissionsThisYear, 1);
  assert.deepEqual(stats.years, [2026, 2025]);
  assert.equal(buildAccountStats(problems, { solved: [], submissions: [] }, local(2026, 1, 1), 2024).days.length, 366);
});
