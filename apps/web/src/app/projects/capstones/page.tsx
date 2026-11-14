import Link from "next/link";
import { getCapstones } from "@/lib/integrated-projects";
import "@/components/integrated-project.css";

export const dynamic = "force-dynamic";
export const metadata = { title: "Robotics capstone projects" };

export default function Page() {
  const projects = getCapstones();
  return <main id="main" className="page collection-page">
    <div className="page-intro"><span className="eyebrow">ROBOTICS CAPSTONES</span><h1>Connect the components.</h1><p>Build a bounded pipeline, evaluate failures, and write a reproducibility report. Each project runs in the existing isolated coding workspace.</p></div>
    {projects.length ? <div className="integration-catalog">{projects.map(project => <article key={project.slug}><span className="eyebrow">{project.stages.length} STAGES + INTEGRATION</span><h2>{project.title}</h2><p>{project.summary}</p><Link className="button secondary" href={`/projects/capstones/${project.slug}`}>Explore project</Link></article>)}</div> : <p>No reviewed capstone projects are available yet.</p>}
  </main>;
}
