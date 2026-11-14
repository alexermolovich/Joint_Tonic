import type { Job, ProblemMeta } from "./types";

type ProgressInput = { solved: string[]; submissions: Job[] };
const dayMs = 86_400_000;

function localDay(date: Date) {
  // UTC is used only to number local calendar dates, so DST cannot create gaps.
  return Math.floor(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) / dayMs);
}

function dateKey(date: Date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

export function buildAccountStats(problems: ProblemMeta[], progress: ProgressInput, now: Date, year = now.getFullYear()) {
  const knownSlugs = new Set(problems.map(problem => problem.slug));
  const uniqueJobs = new Map<string, Job>();
  for (const job of progress.submissions) {
    if (job.mode === "submit" && (job.status === "completed" || job.status === "failed") && !uniqueJobs.has(job.id)) uniqueJobs.set(job.id, job);
  }
  const submissions = [...uniqueJobs.values()].sort((a, b) => (Date.parse(b.created_at) || 0) - (Date.parse(a.created_at) || 0));
  const graded = submissions.filter(job => job.status === "completed" && typeof job.passed === "boolean");
  const accepted = graded.filter(job => job.passed);
  const solvedSlugs = new Set([...progress.solved, ...accepted.map(job => job.slug)].filter(slug => knownSlugs.has(slug)));
  const today = localDay(now);
  const activity = new Map<number, { submissions: number; accepted: number }>();
  const years = new Set([now.getFullYear()]);
  for (const job of submissions) {
    const date = new Date(job.created_at);
    if (!Number.isFinite(date.getTime()) || date.getTime() > now.getTime()) continue;
    const day = localDay(date);
    years.add(date.getFullYear());
    const entry = activity.get(day) || { submissions: 0, accepted: 0 };
    entry.submissions++;
    if (job.status === "completed" && job.passed) entry.accepted++;
    activity.set(day, entry);
  }
  const activeDays = [...activity.keys()].sort((a, b) => a - b);
  let bestStreak = 0;
  let run = 0;
  let previous: number | undefined;
  for (const day of activeDays) {
    run = previous !== undefined && day === previous + 1 ? run + 1 : 1;
    bestStreak = Math.max(bestStreak, run);
    previous = day;
  }
  let currentStreak = 0;
  let cursor = activity.has(today) ? today : today - 1;
  while (activity.has(cursor)) { currentStreak++; cursor--; }

  const start = new Date(year, 0, 1, 12);
  const days = [];
  for (let date = new Date(start); date.getFullYear() === year; date.setDate(date.getDate() + 1)) {
    const entry = activity.get(localDay(date));
    days.push({ date: dateKey(date), month: date.getMonth(), day: date.getDate(), weekday: date.getDay(), submissions: entry?.submissions || 0, accepted: entry?.accepted || 0, future: localDay(date) > today });
  }
  const domains = [...new Set(problems.map(problem => problem.domain))].map(domain => {
    const domainProblems = problems.filter(problem => problem.domain === domain);
    const slugs = new Set(domainProblems.map(problem => problem.slug));
    const records = graded.filter(job => slugs.has(job.slug));
    return { domain, total: domainProblems.length, solved: domainProblems.filter(problem => solvedSlugs.has(problem.slug)).length, accepted: records.filter(job => job.passed).length, needsWork: records.filter(job => !job.passed).length };
  });
  const recentSlugs = new Set<string>();
  const recentAccepted = accepted.filter(job => {
    if (!knownSlugs.has(job.slug) || recentSlugs.has(job.slug) || !Number.isFinite(Date.parse(job.created_at))) return false;
    recentSlugs.add(job.slug);
    return true;
  }).slice(0, 6);

  return {
    solvedSlugs, totalSubmissions: submissions.length, gradedSubmissions: graded.length,
    acceptedSubmissions: accepted.length, platformFailures: submissions.filter(job => job.status === "failed").length,
    acceptanceRate: graded.length ? Math.round(accepted.length / graded.length * 100) : null,
    currentStreak, bestStreak, days, year, years: [...years].sort((a, b) => b - a),
    firstWeekday: start.getDay(), activeDaysThisYear: days.filter(day => day.submissions > 0).length,
    submissionsThisYear: days.reduce((total, day) => total + day.submissions, 0), domains, recentAccepted,
  };
}
