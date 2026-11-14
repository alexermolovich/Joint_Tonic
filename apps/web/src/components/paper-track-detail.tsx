import Link from "next/link";
import { ArrowLeft, ArrowUpRight } from "lucide-react";
import type { PaperTrack } from "@/lib/paper-tracks";
import type { ProblemMeta } from "@/lib/types";
import { TrackSteps } from "./track-steps";
import { paperSectionId } from "@/lib/paper-flow";
import { Markdown } from "./markdown";
import { getPaperIntegration } from "@/lib/integrated-projects";
import { IntegratedProject } from "./integrated-project";
import "./paper-track-detail.css";

export function PaperTrackDetail({ track, problems, assessment }: {track:PaperTrack;problems:ProblemMeta[];assessment:string}) {
  const ready=track.slugs.map(slug=>problems.find(problem=>problem.slug===slug)!).filter(Boolean);
  const integration=getPaperIntegration(track.paper.id);
  return <main id="main" className="page detail-page paper-track-detail">
    <Link className="back-link" href="/tracks"><ArrowLeft size={14}/> All tracks</Link>
    <header><span className="eyebrow">{track.subtitle} · {track.paper.year}</span><h1>{track.title}</h1>
      <p className="lead">{track.description}</p>
      <p>{ready.length} runnable exercises · {track.plannedTitles.length} proposed component exercises · {integration ? "bounded integration available" : "integration and assessment planned"}</p>
      <div className="button-row"><Link className="button secondary" href={"/projects/"+track.paper.id}>Read the paper explanation <ArrowUpRight size={15}/></Link><a className="text-link" href={track.paper.primaryUrl} target="_blank" rel="noreferrer">Primary source <ArrowUpRight size={15}/></a></div>
    </header>
    <section><h2>What you will build</h2><p>Implement the mechanisms below as small, independently testable components, then connect them in a bounded demonstration. Available exercises use their own versioned contracts and fixtures. Completing them does not reproduce the paper’s full model or published benchmark.</p>
      <h3>Prerequisites</h3>{track.prerequisiteSlugs.length ? <ul>{track.prerequisiteSlugs.map(slug=><li key={slug}><Link href={"/problems/"+slug}>{problems.find(problem=>problem.slug===slug)?.title}</Link></li>)}</ul>:<p>Start with the first stage’s observation, shape, unit and coordinate-frame contract. Its paper explanation identifies the required robotics concepts.</p>}
    </section>
    {ready.length>0 ? <section aria-label="Runnable track exercises"><p className="muted">Progress below covers available coding exercises only. Proposed stages and the final assessment are not counted as completed.</p><TrackSteps track={track} problems={ready}/></section>:<section className="empty-state"><h2>Component plan ready</h2><p>This track has no runnable evaluator yet. Read the explanations below; proposed exercises need reviewed contracts, solutions and grading before publication.</p></section>}
    <section><h2>Paper-to-code sequence</h2><ol className="paper-track-stages">{track.paper.executionFlow?.nodes.map(node=><li key={node.id}><h3>{node.title}</h3><p>{node.detail}</p><Link href={"/projects/"+track.paper.id+"#"+paperSectionId(node.section)}>Read this component’s theory and math →</Link><ul>{node.problem_slugs.map(slug=><li key={slug}><Link href={"/problems/"+slug+"?track="+track.slug}>{problems.find(problem=>problem.slug===slug)?.title}</Link> <span className="muted">Runnable</span></li>)}{node.planned_problems?.map(title=><li key={title}>{title} <span className="muted">Proposed · implementation pending</span></li>)}</ul></li>)}</ol></section>
    {integration ? <IntegratedProject project={integration}/> : <section aria-label="Planned integration and assessment"><span className="eyebrow">Planned assessment · no evaluator yet</span>{assessment ? <Markdown>{assessment}</Markdown> : <><h2>Integration and evaluation</h2><p>Connect the ordered components using a small synthetic fixture, trace intermediate values, and compare against an independent reference. Report a failure case and document units, frames, timing, source revision, fixture provenance, seeds and runtime versions. This assessment requires its own reviewed contract.</p></>}</section>}
  </main>;
}
