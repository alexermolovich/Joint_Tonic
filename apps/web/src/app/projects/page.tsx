import { getPapers, getProblems } from "@/lib/content";
import { summarizeProject } from "@/lib/projects";
import { ProjectCatalog } from "@/components/project-catalog";

export const dynamic = "force-dynamic";
export const metadata = { title: "Projects" };

export default function Page() {
  const problems = getProblems();
  return <main id="main" className="page projects-page">
    <ProjectCatalog projects={getPapers().map(paper => summarizeProject(paper, problems))} />
  </main>;
}
