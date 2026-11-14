"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight, CheckCircle2, FileCode2, Flame, Settings2, Target } from "lucide-react";
import { buildAccountStats } from "@/lib/account-stats";
import { useWorkspace } from "@/lib/local-workspace";
import type { ProblemMeta, Track } from "@/lib/types";
import "./account-stats.css";

const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function AccountStats({ problems, tracks }: { problems: ProblemMeta[]; tracks: Track[] }) {
  const { state, ready } = useWorkspace();
  const [now, setNow] = useState<Date | null>(null);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  useEffect(() => { setNow(new Date()); }, []);

  if (!ready || !now) return <main id="main" className="page collection-page jt-account"><h1>Your progress</h1><p role="status">Loading your local workspace…</p></main>;

  const stats = buildAccountStats(problems, state, now, selectedYear ?? now.getFullYear());
  const drafts = problems.filter(problem => state.drafts[problem.slug] && !stats.solvedSlugs.has(problem.slug));
  const activeDays = stats.days.filter(day => day.submissions > 0);
  const weeks = Math.ceil((stats.firstWeekday + stats.days.length) / 7);

  return <main id="main" className="page collection-page jt-account">
    <header className="jt-account-header">
      <div><span className="eyebrow">YOUR ROBOTICS WORKSPACE</span><h1>{state.name ? `${state.name}’s progress` : "Your progress"}</h1><p>Small components. Real progress. Saved on this device.</p></div>
      <Link className="button secondary" href="/settings"><Settings2 size={16} /> Workspace settings</Link>
    </header>

    <section className="jt-account-metrics" aria-label="Progress summary">
      <div className="jt-account-metric"><CheckCircle2 size={19} aria-hidden="true" /><span>Problems solved</span><strong>{stats.solvedSlugs.size}<small> / {problems.length}</small></strong><p>Unique implemented components</p></div>
      <div className="jt-account-metric"><FileCode2 size={19} aria-hidden="true" /><span>Saved submissions</span><strong>{stats.totalSubmissions}</strong><p>{stats.gradedSubmissions} graded · {stats.platformFailures} evaluator errors</p></div>
      <div className="jt-account-metric"><Target size={19} aria-hidden="true" /><span>Acceptance rate</span><strong>{stats.acceptanceRate === null ? "—" : `${stats.acceptanceRate}%`}</strong><p>{stats.acceptedSubmissions} accepted of {stats.gradedSubmissions} graded</p></div>
      <div className="jt-account-metric"><Flame size={19} aria-hidden="true" /><span>Current streak</span><strong>{stats.currentStreak}<small> {stats.currentStreak === 1 ? "day" : "days"}</small></strong><p>Best recorded: {stats.bestStreak} {stats.bestStreak === 1 ? "day" : "days"}</p></div>
    </section>

    <section className="jt-account-panel" aria-labelledby="activity-heading">
      <div className="jt-account-section-heading"><div><h2 id="activity-heading">Your activity</h2><p>{stats.submissionsThisYear} saved submissions across {stats.activeDaysThisYear} active {stats.activeDaysThisYear === 1 ? "day" : "days"} in {stats.year}</p></div><label className="jt-account-year">Year<select value={stats.year} onChange={event => setSelectedYear(Number(event.target.value))}>{stats.years.map(year => <option key={year} value={year}>{year}</option>)}</select></label></div>
      <div className="jt-account-calendar-scroll">
        <div className="jt-account-calendar" style={{ minWidth: weeks * 14 + 30 }} role="img" aria-label={`${stats.year} activity calendar: ${stats.submissionsThisYear} submissions on ${stats.activeDaysThisYear} days. A daily data table is available below.`}>
          <div className="jt-account-months" style={{ gridTemplateColumns: `repeat(${weeks}, 1fr)` }} aria-hidden="true">{stats.days.map((day, index) => day.day === 1 && <span key={day.date} style={{ gridColumn: Math.floor((stats.firstWeekday + index) / 7) + 1 }}>{months[day.month]}</span>)}</div>
          <div className="jt-account-calendar-body" aria-hidden="true"><div className="jt-account-weekdays"><span>Sun</span><span>Tue</span><span>Thu</span><span>Sat</span></div><div className="jt-account-day-grid" style={{ gridTemplateColumns: `repeat(${weeks}, 1fr)` }}>{Array.from({ length: stats.firstWeekday }, (_, index) => <span className="jt-account-day blank" key={`blank-${index}`} />)}{stats.days.map(day => <span key={day.date} className={`jt-account-day level-${Math.min(day.submissions, 4)}${day.future ? " future" : ""}`} title={`${day.date}: ${day.submissions} submissions, ${day.accepted} accepted`} />)}</div></div>
        </div>
      </div>
      <div className="jt-account-calendar-footer"><p>A streak counts consecutive local dates with a saved submission, ending today or yesterday.</p><div className="jt-account-legend" aria-label="Activity colors: zero through four or more submissions"><span>Less</span>{[0, 1, 2, 3, 4].map(level => <i key={level} className={`jt-account-day level-${level}`} aria-hidden="true" />)}<span>More</span></div></div>
      <details className="jt-account-activity-table"><summary>View daily activity as a table</summary>{activeDays.length ? <><p>Dates without saved submissions have zero activity.</p><table><caption>Saved submission activity in {stats.year}</caption><thead><tr><th scope="col">Local date</th><th scope="col">Submissions</th><th scope="col">Accepted</th></tr></thead><tbody>{activeDays.map(day => <tr key={day.date}><th scope="row">{day.date}</th><td>{day.submissions}</td><td>{day.accepted}</td></tr>)}</tbody></table></> : <p>No saved activity in {stats.year}. Submit a solution to start your activity record.</p>}</details>
    </section>

    <p className="jt-account-history-note">Submission counts, acceptance, activity and streaks reflect your latest 100 saved submissions. Solved totals are retained separately. Evaluator errors are excluded from acceptance and domain results.</p>

    <div className="jt-account-two-columns">
      <section className="jt-account-panel" aria-labelledby="domains-heading"><div className="jt-account-section-heading"><div><h2 id="domains-heading">Across robotics</h2><p>Graded submissions by domain</p></div></div><div className="jt-account-domain-key"><span><i className="accepted" />Accepted</span><span><i className="needs-work" />Needs work</span></div><div className="jt-account-domains">{stats.domains.map(domain => { const total = domain.accepted + domain.needsWork; return <div className="jt-account-domain" key={domain.domain}><div><h3>{domain.domain}</h3><span>{domain.solved} / {domain.total} solved</span></div><div className="jt-account-domain-bar" role="img" aria-label={`${domain.domain}: ${domain.accepted} accepted, ${domain.needsWork} need work`}><i className="accepted" style={{ width: total ? `${domain.accepted / total * 100}%` : "0%" }} /><i className="needs-work" style={{ width: total ? `${domain.needsWork / total * 100}%` : "0%" }} /></div><p>{domain.accepted} accepted <span>·</span> {domain.needsWork} need work</p></div>; })}</div></section>

      <section className="jt-account-panel" aria-labelledby="recent-heading"><div className="jt-account-section-heading"><div><h2 id="recent-heading">Recently solved</h2><p>Your latest accepted components</p></div></div>{stats.recentAccepted.length ? <div className="jt-account-recent">{stats.recentAccepted.map(job => { const problem = problems.find(item => item.slug === job.slug)!; return <Link key={job.id} href={`/submissions/${job.id}`} className="jt-account-recent-row"><CheckCircle2 size={18} aria-hidden="true" /><div><strong>{problem.title}</strong><span>{problem.domain} · {new Date(job.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}</span></div><ArrowRight size={15} aria-hidden="true" /></Link>; })}</div> : <div className="jt-account-empty"><CheckCircle2 size={27} aria-hidden="true" /><h3>Your first component starts here.</h3><p>Accepted submissions in your saved history will appear here.</p><Link className="text-link" href="/problems">Find a problem <ArrowRight size={15} /></Link></div>}</section>
    </div>

    <section className="jt-account-paths" aria-labelledby="paths-heading"><div className="jt-account-section-heading"><div><h2 id="paths-heading">Your learning paths</h2><p>Build one component at a time.</p></div><Link className="text-link" href="/tracks">Explore paths <ArrowRight size={15} /></Link></div><div className="jt-account-track-grid">{tracks.map(track => { const count = track.slugs.filter(slug => stats.solvedSlugs.has(slug)).length; const next = track.slugs.find(slug => !stats.solvedSlugs.has(slug)) || track.slugs[0]; return <article className="jt-account-panel jt-account-track" key={track.slug}><span className="eyebrow">{track.subtitle}</span><h3>{track.title}</h3><p>{count} / {track.slugs.length} components solved</p><progress max={track.slugs.length || 1} value={count} aria-label={`${track.title}: ${count} of ${track.slugs.length} solved`} /><Link className="text-link" href={next ? `/problems/${next}?track=${track.slug}` : `/tracks/${track.slug}`}>{count === track.slugs.length ? "Review path" : count ? "Continue learning" : "Start learning"}<ArrowRight size={15} /></Link></article>; })}</div></section>

    {drafts.length > 0 && <section className="jt-account-panel" aria-labelledby="drafts-heading"><div className="jt-account-section-heading"><div><h2 id="drafts-heading">On your workbench</h2><p>{drafts.length} saved {drafts.length === 1 ? "draft" : "drafts"} ready to continue</p></div></div><div className="jt-account-drafts">{drafts.map(problem => <Link className="jt-account-recent-row" key={problem.slug} href={`/problems/${problem.slug}`}><FileCode2 size={18} aria-hidden="true" /><div><strong>{problem.title}</strong><span>{problem.domain} · draft saved</span></div><ArrowRight size={15} aria-hidden="true" /></Link>)}</div></section>}
  </main>;
}
