"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { ArrowRight, Search } from "lucide-react";
import { projectSheet, projectSheets } from "@/lib/projects";
import { useWorkspace } from "@/lib/local-workspace";
import type { Paper, ProblemMeta } from "@/lib/types";
import "./paper-track-catalog.css";

export function PaperTrackCatalog({ papers, problems }: { papers: Paper[]; problems: ProblemMeta[] }) {
  const searchParams = useSearchParams();
  const topicParam = searchParams.get("topic");
  const requestedTopic = projectSheets.some(sheet => sheet.slug === topicParam) || topicParam === "other" ? topicParam! : "all";
  const [query, setQuery] = useState("");
  const [topic, setTopic] = useState(requestedTopic);
  const [availability, setAvailability] = useState("all");
  const { state, ready } = useWorkspace();
  useEffect(() => { setTopic(requestedTopic); }, [requestedTopic]);
  const tracks = useMemo(() => {
    const known = new Map(problems.map(problem => [problem.slug, problem]));
    return papers.map(paper => {
      const nodes = paper.executionFlow?.nodes || [];
      const slugs = [...new Set(nodes.flatMap(node => node.problem_slugs))].filter(slug => known.has(slug));
      const planned = [...new Set(nodes.flatMap(node => node.planned_problems || []))];
      const sheet = projectSheet(paper.category);
      return {
        paper, slugs, planned, stages: nodes.length, topic: sheet?.slug || "other",
        topicTitle: sheet?.title || "Other research",
        search: [paper.title, paper.id, paper.category, sheet?.title, ...paper.topics,
          ...nodes.map(node => node.title), ...planned, ...slugs.map(slug => known.get(slug)?.title)].join(" ").toLowerCase(),
      };
    }).sort((a, b) => Number(b.slugs.length > 0) - Number(a.slugs.length > 0)
      || b.paper.year - a.paper.year || a.paper.title.localeCompare(b.paper.title));
  }, [papers, problems]);
  const normalizedQuery = query.trim().toLowerCase();
  const matches = tracks.filter(track => (topic === "all" || track.topic === topic)
    && (availability === "all" || (availability === "runnable" ? track.slugs.length > 0 : track.slugs.length === 0 && track.planned.length > 0))
    && track.search.includes(normalizedQuery));
  const topics = [...projectSheets.map(sheet => ({ slug: sheet.slug, title: sheet.title })), { slug: "other", title: "Other research" }]
    .filter(sheet => tracks.some(track => track.topic === sheet.slug));
  const solvedSlugs = new Set(state.solved);
  const clearFilters = () => { setQuery(""); setTopic("all"); setAvailability("all"); };

  return <section className="paper-track-catalog" aria-labelledby="paper-track-heading">
    <header className="paper-track-intro">
      <h2 id="paper-track-heading">Research paper tracks</h2>
      <p>Follow each paper’s model stages and implement its components. Progress counts runnable problems; planned components show what comes next.</p>
    </header>
    <div className="paper-track-filters">
      <label className="paper-track-search"><Search size={18} aria-hidden="true" /><input type="search" aria-label="Search paper tracks" placeholder="Search papers or implementation components…" value={query} onChange={event => setQuery(event.target.value)} /></label>
      <label className="paper-track-select"><span>Topic</span><select aria-label="Topic" value={topic} onChange={event => setTopic(event.target.value)}><option value="all">All topics</option>{topics.map(sheet => <option key={sheet.slug} value={sheet.slug}>{sheet.title}</option>)}</select></label>
      <label className="paper-track-select"><span>Availability</span><select aria-label="Availability" value={availability} onChange={event => setAvailability(event.target.value)}><option value="all">All tracks</option><option value="runnable">Runnable problems available</option><option value="planned">Planned only</option></select></label>
    </div>
    <p className="paper-track-result-count" role="status">{matches.length} {matches.length === 1 ? "paper track" : "paper tracks"}</p>
    {topics.map(sheet => {
      const group = matches.filter(track => track.topic === sheet.slug);
      if (!group.length) return null;
      return <section className="paper-track-group" key={sheet.slug} aria-labelledby={`paper-track-topic-${sheet.slug}`}>
        <h3 id={`paper-track-topic-${sheet.slug}`}>{sheet.title}<span>{group.length}</span></h3>
        <div className="paper-track-grid">{group.map(track => {
          const solved = track.slugs.filter(slug => solvedSlugs.has(slug)).length;
          return <Link className="paper-track-card" href={`/tracks/paper-${track.paper.id}`} key={track.paper.id}>
            <div className="paper-track-card-meta"><span>{track.paper.year}</span><span className={track.slugs.length ? "paper-track-available" : ""}>{track.slugs.length ? "Ready to code" : track.planned.length ? "Planned components" : "Track in preparation"}</span></div>
            <h4>{track.paper.title}</h4>
            <p className="paper-track-topic">{track.topicTitle}</p>
            <div className="paper-track-counts"><span>{track.stages} model {track.stages === 1 ? "stage" : "stages"}</span><span>{track.slugs.length} runnable</span><span>{track.planned.length} planned</span></div>
            <div className="paper-track-card-footer"><span>{track.slugs.length ? ready ? `${solved} / ${track.slugs.length} runnable problems solved` : "Loading progress…" : "Coding problems coming next"}</span><ArrowRight size={17} aria-hidden="true" /></div>
          </Link>;
        })}</div>
      </section>;
    })}
    {!matches.length && <div className="paper-track-empty"><h3>{papers.length ? "No paper tracks match" : "Paper tracks are in preparation"}</h3><p>{papers.length ? "Try another paper, component, or topic." : "Collected papers will appear here with their implementation stages."}</p>{papers.length > 0 && <button type="button" className="button secondary" onClick={clearFilters}>Clear filters</button>}</div>}
  </section>;
}
