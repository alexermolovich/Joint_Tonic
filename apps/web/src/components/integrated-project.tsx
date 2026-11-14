import Link from "next/link";
import { ArrowRight, Code2 } from "lucide-react";
import { getProblems } from "@/lib/content";
import type { IntegratedProject as Project } from "@/lib/integrated-projects";
import { Markdown } from "./markdown";
import { PaperReaderProgress } from "./paper-reader-progress";
import "./integrated-project.css";

export function IntegratedProject({ project, headingLevel = 2 }: { project: Project; headingLevel?: 1 | 2 }) {
  const problems = getProblems();
  const integration = problems.find(problem => problem.slug === project.integrationProblemSlug)!;
  const Heading = headingLevel === 1 ? "h1" : "h2";
  return <section className="integration-project" aria-label={`${project.title} implementation project`}>
    <div className="integration-launch">
      <div><span className="eyebrow">RUNNABLE INTEGRATION · v{project.version}</span><Heading>{project.title}</Heading><p>{project.summary}</p><PaperReaderProgress problems={[integration]} showAction={false} /></div>
      <Link className="button primary" href={`/problems/${integration.slug}`}><Code2 size={17} /> Open integration editor <ArrowRight size={15} /></Link>
    </div>
    <Markdown>{project.orientation.replace(/^# /, "## ")}</Markdown>
    <h2>Build the pipeline</h2>
    <ol className="integration-stages">
      {project.stages.map((stage, index) => <li key={`${index}-${stage.title}`}>
        <div className="integration-step" aria-hidden="true">{index + 1}</div>
        <div><h3>{stage.title}</h3><p>{stage.description}</p><ul>{stage.problemSlugs.map(slug => <li key={slug}><Link href={`/problems/${slug}`}>{problems.find(problem => problem.slug === slug)!.title}</Link></li>)}</ul></div>
      </li>)}
      <li><div className="integration-step" aria-hidden="true">{project.stages.length + 1}</div><div><h3>Integrate and test</h3><p>Compose the stages in one bounded function, inspect failures, and submit against the complete contract.</p><Link className="text-link" href={`/problems/${integration.slug}`}>{integration.title} <ArrowRight size={14} /></Link></div></li>
    </ol>
    <details className="integration-detail" open><summary>Evaluation and failure analysis</summary><Markdown>{project.evaluation}</Markdown></details>
    <details className="integration-detail"><summary>Reproducibility report template</summary><Markdown>{project.reproducibility}</Markdown><Link className="button secondary" href={`/problems/${integration.slug}`}>Open workspace and save your report in Notes</Link></details>
  </section>;
}
