import fs from "node:fs";
import path from "node:path";
import { cache } from "react";
import { getProblems, repoRoot } from "./content";

export type IntegratedProject = {
  slug: string;
  title: string;
  summary: string;
  version: string;
  integrationProblemSlug: string;
  paperIds: string[];
  stages: { title: string; description: string; problemSlugs: string[] }[];
  orientation: string;
  evaluation: string;
  reproducibility: string;
};

const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
function loadProject(folder: "capstones" | "paper-projects", slug: string): IntegratedProject | null {
  if (!slugPattern.test(slug)) return null;
  const directory = path.join(repoRoot(), "content", folder, slug);
  const file = path.join(directory, "meta.json");
  if (!fs.existsSync(file)) return null;
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  const known = new Set(getProblems().map(problem => problem.slug));
  const strings = (value: unknown): value is string[] => Array.isArray(value) && value.every(item => typeof item === "string" && slugPattern.test(item));
  if (data.slug !== slug || ![data.title, data.summary, data.version].every(value => typeof value === "string" && value.trim()) ||
      !known.has(data.integrationProblemSlug) || !strings(data.paperIds) || !Array.isArray(data.stages) || !data.stages.length ||
      !data.stages.every((stage: { title?: unknown; description?: unknown; problemSlugs?: unknown }) => typeof stage.title === "string" && typeof stage.description === "string" && strings(stage.problemSlugs) && stage.problemSlugs.every(id => known.has(id)))) {
    throw new Error(`Invalid integrated project contract: ${folder}/${slug}`);
  }
  const read = (name: string) => fs.readFileSync(path.join(directory, `${name}.md`), "utf8");
  return { ...data, orientation: read("orientation"), evaluation: read("evaluation"), reproducibility: read("reproducibility") };
}

export const getCapstone = cache((slug: string) => loadProject("capstones", slug));
export const getPaperIntegration = cache((paperId: string) => loadProject("paper-projects", paperId));
export const getCapstones = cache(() => {
  const directory = path.join(repoRoot(), "content/capstones");
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory).map(getCapstone).filter((project): project is IntegratedProject => project !== null);
});
