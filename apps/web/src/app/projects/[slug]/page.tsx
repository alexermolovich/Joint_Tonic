import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { ArrowRight, ArrowUpRight, FileCode2 } from "lucide-react";
import { getPapers, getProblems, tracks } from "@/lib/content";
import { findProject, linkedProjectProblems, projectSheet } from "@/lib/projects";
import { Markdown } from "@/components/markdown";
import { PaperExecutionFlow } from "@/components/paper-execution-flow";
import { PaperReaderProgress } from "@/components/paper-reader-progress";
import { getPaperIntegration } from "@/lib/integrated-projects";
import { IntegratedProject } from "@/components/integrated-project";
import "@/components/projects.css";
import "@/components/paper-reader.css";

export const dynamic = "force-dynamic";
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return { title: findProject(getPapers(), slug)?.title || "Project" };
}
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const papers = getPapers();
  const paper = findProject(papers, slug);
  if (!paper) notFound();
  if (paper.id !== slug) redirect(`/projects/${paper.id}`);
  const allProblems = getProblems();
  const problems = linkedProjectProblems(paper, allProblems);
  const relatedTracks = tracks.filter(track => track.slugs.some(id => problems.some(problem => problem.slug === id)));
  const sheet = projectSheet(paper.category);
  const integration = getPaperIntegration(paper.id);
  return <main id="main" className="paper-reader-page">
    <div className="paper-reader-content">
      <header className="paper-detail-header">
        <div className="eyebrow">{sheet?.title || "Paper project"} / {paper.year}</div><h1>{paper.title}</h1>
        <p className="paper-authors">{paper.authors.join(", ")}</p>
        <p className="project-scope">{paper.executionFlow?.description || "This paper is part of our project roadmap. Its guided explanation and implementation sequence are being prepared."}</p>
        <div className="paper-reader-progress">
          {paper.executionFlow && <span>{paper.executionFlow.nodes.length} model stages</span>}
          <a className="paper-reader-source" target="_blank" rel="noreferrer" href={paper.primaryUrl}>Original paper <ArrowUpRight size={14} /></a>
          <PaperReaderProgress problems={problems} />
        </div>
      </header>
      {paper.executionFlow && <PaperExecutionFlow flow={paper.executionFlow} paperId={paper.id} problems={allProblems} />}
      {integration && <IntegratedProject project={integration} />}
      <section className="paper-reader-material" aria-label="Paper explanation and mathematics">
        {paper.executionFlow ? <Markdown paperAnchors>{paper.content.replace(/^# [^\n]+\r?\n/, "")}</Markdown> : <div className="project-preparing"><h2>Project in preparation</h2><p>The source paper is available above. We are developing an original explanation with mathematics, a model execution graph, and links to practical exercises. Available related problems appear below.</p></div>}
      </section>
      <section className="paper-reader-practice" aria-labelledby="project-practice-heading">
        <h2 id="project-practice-heading">Practice the components</h2>
        {problems.length ? <><p>These exercises cover selected components and prerequisites. Completing them is not a full paper reproduction.</p><div className="paper-reader-problems">{problems.map(problem => <Link className="paper-problem-link" key={problem.slug} href={`/problems/${problem.slug}`}><FileCode2 size={17} /><span>{problem.title}<small>{problem.difficulty} · {problem.framework} · {problem.minutes} min</small></span><ArrowUpRight size={13} /></Link>)}</div></> : <p>Coding exercises will appear here as their problem contracts and evaluators become available.</p>}
        <div className="paper-reader-tracks">{relatedTracks.map(track => <Link className="button secondary" href={`/tracks/${track.slug}`} key={track.slug}>{track.title} <ArrowRight size={13} /></Link>)}</div>
      </section>
    </div>
  </main>;
}
