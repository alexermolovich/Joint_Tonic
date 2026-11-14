import { getPapers, getProblems } from "@/lib/content";
import { summarizeProject } from "@/lib/projects";
import { ProjectCatalog } from "@/components/project-catalog";
import Link from "next/link";
import "@/components/integrated-project.css";

export const dynamic = "force-dynamic";
export const metadata = { title: "Projects" };

export default function Page() {
  const problems = getProblems();
  return <main id="main" className="page projects-page">
    <div className="integration-index-link"><div><strong>Build complete robotics pipelines</strong><br /><span>Four runnable capstones connect perception, policy adaptation, edge deployment, and sim-to-real evidence.</span></div><Link className="button secondary" href="/projects/capstones">Explore capstones</Link></div>
    <ProjectCatalog projects={getPapers().map(paper => summarizeProject(paper, problems))} />
  </main>;
}
