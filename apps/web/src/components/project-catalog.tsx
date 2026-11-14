"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight, Search, FileCode2 } from "lucide-react";
import { projectSheets, type ProjectSummary } from "@/lib/projects";
import { useWorkspace } from "@/lib/local-workspace";
import "./projects.css";

export function ProjectCatalog({ projects, sheet }: { projects: ProjectSummary[]; sheet?: string }) {
  const [query, setQuery] = useState("");
  const [availability, setAvailability] = useState("all");
  const currentSheet = projectSheets.find(item => item.slug === sheet);
  const { state, ready } = useWorkspace();
  const matches = projects.filter(project => (!sheet || project.sheet === sheet)
    && (availability === "all" || (availability === "coding" ? project.problems.length > 0 : project.stages > 0))
    && `${project.title} ${project.authors} ${project.topics.join(" ")}`.toLowerCase().includes(query.trim().toLowerCase()))
    .sort((a, b) => Number(b.problems.length > 0) - Number(a.problems.length > 0) || Number(b.stages > 0) - Number(a.stages > 0) || b.year - a.year || a.title.localeCompare(b.title));

  return <section className="project-results" aria-labelledby="project-list-heading">
      <header className="projects-intro"><h1 id="project-list-heading">{currentSheet?.title || "Projects"}</h1><p>{currentSheet?.description || "Build your understanding of physical AI, one paper component at a time. Explore the model, follow the math, and implement the pieces in your coding workspace."}</p></header>
      <div className="project-filters"><label className="search-field"><Search size={18} aria-hidden="true" /><input aria-label="Search projects" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search models, papers, or robotics concepts…" /></label><select aria-label="Project availability" value={availability} onChange={event => setAvailability(event.target.value)}><option value="all">All projects</option><option value="coding">With coding problems</option><option value="theory">With model explanations</option></select></div>
      <p className="project-result-count" role="status">{matches.length} {matches.length === 1 ? "project" : "projects"} · Linked problems include prerequisites and related components.</p>
      <div className="project-grid">{matches.map(project => <Link className="project-card" href={`/projects/${project.id}`} key={project.id}>
        <div className="project-card-top"><span>{project.year}</span><span className={project.problems.length ? "project-status available" : "project-status"}>{project.problems.length ? "Coding components available" : project.stages ? "Model explanation available" : "In preparation"}</span></div>
        <h3>{project.title}</h3><p>{project.description}</p>
        <div className="project-tags">{project.topics.slice(0, 2).map(topic => <span key={topic}>{topic}</span>)}</div>
        <div className="project-card-footer"><span>{project.stages ? `${project.stages} model stages` : "Source collected"}{project.problems.length > 0 && <> · {project.problems.length} linked {project.problems.length === 1 ? "problem" : "problems"}</>}</span><ArrowRight size={17} aria-hidden="true" /></div>
        {project.problems.length > 0 && <div className="project-coding-summary"><span>{ready ? `${project.problems.filter(problem => state.solved.includes(problem.slug)).length}/${project.problems.length} linked problems solved` : "Loading progress…"}</span><span>{["Easy", "Medium", "Hard"].map(level => { const count = project.problems.filter(problem => problem.difficulty === level).length; return count ? `${count} ${level}` : null; }).filter(Boolean).join(" · ")}</span></div>}
      </Link>)}</div>
      {!matches.length && <div className="empty-state"><FileCode2 size={28} /><h3>No projects match these filters</h3><p>Try another search or include projects in preparation.</p><button className="button secondary" onClick={() => { setQuery(""); setAvailability("all"); }}>Clear filters</button></div>}
  </section>;
}
