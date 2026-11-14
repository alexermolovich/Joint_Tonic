"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { useWorkspace } from "@/lib/local-workspace";
import type { ProblemMeta } from "@/lib/types";

export function PaperReaderProgress({ problems, showAction = true }: { problems: ProblemMeta[]; showAction?: boolean }) {
  const { state, ready } = useWorkspace();
  if (!problems.length) return <span>Coding components in preparation</span>;
  const solved = problems.filter(problem => state.solved.includes(problem.slug)).length;
  const next = problems.find(problem => !state.solved.includes(problem.slug)) || problems[0];
  return <><span>{ready ? `${solved} / ${problems.length} linked problems solved` : `${problems.length} linked coding problems`}</span>{showAction && <Link className="button primary" href={`/problems/${next.slug}`}>{ready && solved === problems.length ? "Review components" : "Continue coding"}<ArrowRight size={15} /></Link>}</>;
}
