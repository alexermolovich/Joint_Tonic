import { notFound } from "next/navigation";
import { getPapers, getProblems } from "@/lib/content";
import { projectSheets, summarizeProject } from "@/lib/projects";
import { ProjectCatalog } from "@/components/project-catalog";

export const dynamic = "force-dynamic";
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return { title: projectSheets.find(sheet => sheet.slug === slug)?.title || "Project topic" };
}
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const sheet = projectSheets.find(item => item.slug === slug);
  if (!sheet) notFound();
  const problems = getProblems();
  return <main id="main" className="page projects-page">
    <ProjectCatalog sheet={sheet.slug} projects={getPapers().map(paper => summarizeProject(paper, problems))} />
  </main>;
}
