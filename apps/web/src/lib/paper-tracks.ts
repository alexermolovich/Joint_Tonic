import type { Paper, ProblemMeta, Track } from "./types";
import { projectSheet } from "./projects.ts";

export type PaperTrack = Track & { paper: Paper; plannedTitles: string[]; prerequisiteSlugs: string[] };

export function buildPaperTracks(papers: Paper[], problems: ProblemMeta[]): PaperTrack[] {
  const known = new Set(problems.map(problem => problem.slug));
  return papers.map(paper => {
    const stages = paper.executionFlow?.nodes || [];
    const slugs = [...new Set(stages.flatMap(node => node.problem_slugs))].filter(slug => known.has(slug));
    const plannedTitles = [...new Set(stages.flatMap(node => node.planned_problems || []))];
    const prerequisiteSlugs = [...new Set(problems.filter(problem => slugs.includes(problem.slug)).flatMap(problem => problem.prerequisites))].filter(slug => known.has(slug) && !slugs.includes(slug));
    return { slug: `paper-${paper.id}`, title: paper.title, subtitle: projectSheet(paper.category)?.title || "Research paper", description: paper.executionFlow?.description || paper.brief, icon: "book", color: "orange", slugs, objectives: stages.map(node => node.title), paper, plannedTitles, prerequisiteSlugs };
  });
}
