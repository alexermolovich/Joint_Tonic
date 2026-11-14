import { notFound, redirect } from "next/navigation";
import { getPapers } from "@/lib/content";
import { findProject } from "@/lib/projects";

export const dynamic = "force-dynamic";
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const paper = findProject(getPapers(), slug);
  if (!paper) notFound();
  redirect(`/projects/${paper.id}`);
}
