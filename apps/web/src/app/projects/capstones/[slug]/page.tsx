import Link from "next/link";
import { notFound } from "next/navigation";
import { getCapstone } from "@/lib/integrated-projects";
import { IntegratedProject } from "@/components/integrated-project";

export const dynamic = "force-dynamic";
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return { title: getCapstone(slug)?.title || "Capstone project" };
}
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const project = getCapstone(slug);
  if (!project) notFound();
  return <main id="main" className="page collection-page"><Link href="/projects/capstones" className="text-link">All capstone projects</Link><IntegratedProject project={project} headingLevel={1} /></main>;
}
