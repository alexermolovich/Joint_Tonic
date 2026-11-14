"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowRight, ArrowUpRight, Bookmark, BookOpen, CheckCircle2, Circle, Code2, Search, X } from "lucide-react";
import type { ProblemMeta, Track } from "@/lib/types";
import { useWorkspace } from "@/lib/local-workspace";
import { RoboticsIcon, RuntimeIcon } from "./robotics-icons";
import { LearningPathCards } from "./learning-path-cards";
import "./catalog.css";

const difficulties = ["All difficulties", "Easy", "Medium", "Hard"];
const statuses = ["All status", "Solved", "Unsolved"];
const sorts = ["Recommended", "Difficulty", "Shortest first"];

export function Catalog({ problems, systems = false, tracks = [] }: { problems: ProblemMeta[]; systems?: boolean; tracks?: Track[] }) {
  const params = useSearchParams();
  const { state } = useWorkspace();
  const base = systems ? problems.filter(problem => problem.domain === "MLOps") : problems;
  const domains = ["All topics", ...new Set(base.map(problem => problem.domain))];
  const frameworks = ["All", ...new Set(base.map(problem => problem.framework))];
  function selected(key: string, options: string[]) {
    const value = params.get(key);
    return value && options.includes(value) ? value : options[0];
  }
  const q = params.get("q") || "";
  const domain = selected("domain", domains);
  const framework = selected("framework", frameworks);
  const difficulty = selected("difficulty", difficulties);
  const status = selected("status", statuses);
  const simulator = selected("simulator", ["all", "mujoco"]);
  const sort = selected("sort", sorts);
  const path = systems ? "/systems" : "/problems";

  function filter(key: string, value: string, defaultValue = "") {
    const next = new URLSearchParams(window.location.search);
    if (!value || value === defaultValue) next.delete(key);
    else next.set(key, value);
    const search = next.toString();
    // Native history updates keep this client-side catalog fast and its filters shareable.
    window.history.replaceState(null, "", `${path}${search ? `?${search}` : ""}`);
  }
  function clearFilters() {
    window.history.replaceState(null, "", path);
  }

  const visible = base.filter(problem =>
    (domain === "All topics" || problem.domain === domain) &&
    (framework === "All" || problem.framework === framework) &&
    (simulator === "all" || problem.simulator?.backend === simulator) &&
    (difficulty === "All difficulties" || problem.difficulty === difficulty) &&
    (status === "All status" || (status === "Solved" ? state.solved.includes(problem.slug) : !state.solved.includes(problem.slug))) &&
    `${problem.title} ${problem.summary} ${problem.topics.join(" ")} ${problem.framework} ${problem.paperIds.join(" ")}`.toLowerCase().includes(q.toLowerCase().trim())
  ).sort((a, b) => sort === "Difficulty"
    ? difficulties.indexOf(a.difficulty) - difficulties.indexOf(b.difficulty) || a.number - b.number
    : sort === "Shortest first" ? a.minutes - b.minutes || a.number - b.number : a.number - b.number);
  const solved = base.filter(problem => state.solved.includes(problem.slug)).length;
  const percentage = base.length ? Math.round(solved / base.length * 100) : 0;
  const filtered = !!q || domain !== "All topics" || framework !== "All" || simulator !== "all" || difficulty !== "All difficulties" || status !== "All status";
  const nextProblem = base.find(problem => !state.solved.includes(problem.slug));

  return <main id="main" className="page jt-catalog">
    <header className="jt-catalog-intro">
      <div>
        <span className="jt-kicker"><span /> LEARN BY BUILDING</span>
        <h1>{systems ? "Robotics systems problems" : "Physical AI problems"}<span>.</span></h1>
        <p>{systems ? "Build reliable data and deployment workflows for machines in the real world." : "Understand the idea. Implement the component. See what makes a robot work."}</p>
      </div>
      <Link href="/tracks" className="jt-track-shortcut">Explore learning paths <ArrowUpRight size={16} /></Link>
    </header>

    <LearningPathCards tracks={tracks} problems={problems} />

    <div className="jt-topics" role="group" aria-label="Filter by topic">
      {domains.map(name => {
        return <button key={name} aria-pressed={domain === name} onClick={() => filter("domain", name, "All topics")}>
          <RoboticsIcon topic={name} size={18} /><span>{name}</span><small>{name === "All topics" ? base.length : base.filter(problem => problem.domain === name).length}</small>
        </button>;
      })}
    </div>

    <div className="jt-catalog-grid">
      <section className="jt-problem-collection" aria-label="Problem collection">
        <div className="jt-frameworks" role="group" aria-label="Filter by framework">
          {frameworks.map(name => <button key={name} aria-pressed={framework === name} onClick={() => filter("framework", name, "All")}>
            {name !== "All" && <RuntimeIcon framework={name} />}{name === "All" ? "All problems" : name}
            <small>{name === "All" ? base.length : base.filter(problem => problem.framework === name).length}</small>
          </button>)}
          <span className="jt-cpu-label"><span /> CPU ready</span>
        </div>
        <div className="jt-filters">
          <label className="jt-search"><Search size={17} /><input aria-label="Search problems" placeholder="Search problems, concepts, papers…" value={q} onChange={event => filter("q", event.target.value)} />{q && <button aria-label="Clear search" onClick={() => filter("q", "")}><X size={15} /></button>}</label>
          <select aria-label="Filter difficulty" value={difficulty} onChange={event => filter("difficulty", event.target.value, difficulties[0])}>{difficulties.map(value => <option key={value}>{value}</option>)}</select>
          <select aria-label="Filter solve status" value={status} onChange={event => filter("status", event.target.value, statuses[0])}>{statuses.map(value => <option key={value}>{value}</option>)}</select>
          <select aria-label="Filter simulator" value={simulator} onChange={event => filter("simulator", event.target.value, "all")}><option value="all">All simulators</option><option value="mujoco">MuJoCo</option></select>
        </div>
        <div className="jt-results-caption">
          <span role="status" aria-live="polite"><strong>{visible.length}</strong> {visible.length === 1 ? "problem" : "problems"}{filtered && <button onClick={clearFilters}>Clear filters <X size={11} /></button>}</span>
          <label>Sort by <select aria-label="Sort problems" value={sort} onChange={event => filter("sort", event.target.value, sorts[0])}>{sorts.map(value => <option key={value}>{value}</option>)}</select></label>
        </div>
        <div className="jt-table">
          <div className="jt-table-heading" aria-hidden="true"><span /><span>PROBLEM</span><span>DIFFICULTY</span><span>TIME</span><span /></div>
          <ul className="jt-problem-list">
            {visible.map(problem => {
              const isSolved = state.solved.includes(problem.slug);
              return <li key={problem.slug}><Link href={`/problems/${problem.slug}`} className="jt-problem-row">
                <span className={`jt-solve-status ${isSolved ? "is-solved" : ""}`} role="img" aria-label={isSolved ? "Solved" : "Unsolved"}>{isSolved ? <CheckCircle2 size={18} /> : <Circle size={17} />}</span>
                <div className="jt-problem-identity"><span className="jt-topic-tile"><RoboticsIcon topic={problem.domain} size={22} /></span><div className="jt-problem-name"><strong><span className="jt-problem-number">{String(problem.number).padStart(2, "0")}</span><span className="jt-problem-title">{problem.title}</span>{state.bookmarks.includes(problem.slug) && <Bookmark size={12} aria-label="Bookmarked" />}</strong><div><span>{problem.domain}</span><i>·</i><span>{problem.framework}</span>{problem.paperIds.length > 0 && <span className="jt-paper-label"><BookOpen size={10} /> Paper component</span>}</div></div></div>
                <span className={`jt-difficulty ${problem.difficulty.toLowerCase()}`}><i />{problem.difficulty}</span>
                <span className="jt-time">{problem.minutes} <small>min</small></span><ArrowUpRight className="jt-row-arrow" size={16} />
              </Link></li>;
            })}
          </ul>
          {!visible.length && <div className="jt-empty"><Search size={28} /><h2>No matching problems</h2><p>Try another topic or remove a filter to see more of the collection.</p><button className="button secondary" onClick={clearFilters}>Clear filters</button></div>}
        </div>
        <div className="jt-table-footer"><span>Small components. Real understanding.</span><span>{visible.length} of {base.length}</span></div>
      </section>

      <aside className="jt-catalog-sidebar" aria-label="Learning progress and next steps">
        <section className="jt-progress-box">
          <div className="jt-sidebar-heading"><h2>Your progress</h2><span>{percentage}%</span></div>
          <div className="jt-progress-total"><strong>{solved}</strong><span>/ {base.length}</span></div><p>components implemented</p>
          <div className="jt-progress-meter" role="progressbar" aria-label="Problems completed" aria-valuemin={0} aria-valuemax={base.length || 1} aria-valuenow={solved}><span style={{ width: `${percentage}%` }} /></div>
          <div className="jt-progress-levels">{difficulties.slice(1).map(name => <div key={name}><span className={`jt-difficulty ${name.toLowerCase()}`}><i />{name}</span><span>{base.filter(problem => problem.difficulty === name && state.solved.includes(problem.slug)).length}<small> / {base.filter(problem => problem.difficulty === name).length}</small></span></div>)}</div>
          <Link href="/progress" className="jt-sidebar-link">Open your workspace <ArrowRight size={14} /></Link>
        </section>
        <section className="jt-path-box"><span className="jt-path-icon"><RoboticsIcon topic={systems ? "MLOps" : "Robot learning"} size={27} /></span><span className="jt-kicker">ONE COMPONENT AT A TIME</span><h2>{systems ? "Build confidence in the system." : "Start with a frame. Build toward a robot."}</h2><p>{systems ? "Follow the data, check the evidence, and make the release decision." : "Follow a learning path from coordinate transforms to perception and policies."}</p><Link href={systems ? "/tracks/robot-mlops" : "/tracks/robot-perception-foundations"}>Follow the path <ArrowUpRight size={15} /></Link></section>
        {nextProblem && <div className="jt-next-problem"><span className="jt-kicker">YOUR NEXT COMPONENT</span><Link href={`/problems/${nextProblem.slug}`}>{nextProblem.title}<ArrowUpRight size={14} /></Link><p>{nextProblem.difficulty} <span>·</span> {nextProblem.minutes} min</p></div>}
        <div className="jt-browser-note"><Code2 size={15} /><p>Your drafts and progress stay in this browser. No robot required.</p></div>
      </aside>
    </div>
  </main>;
}
