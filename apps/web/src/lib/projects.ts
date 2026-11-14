import type { Paper, ProblemMeta } from "./types";

export const projectSheets = [
  { slug: "perception", title: "Computer vision & perception", description: "Decode detections, understand image features, and reconstruct the world in 3D.", icon: "scan", categories: ["vision-vlm-3d", "perception-3d"] },
  { slug: "vla", title: "Vision-language-action models", description: "Connect visual observations and instructions to robot actions and policy outputs.", icon: "bot", categories: ["vla-embodied", "vla-generalist"] },
  { slug: "mlops", title: "Robotics MLOps & datasets", description: "Validate robot episodes, evaluate edge models, and build reproducible deployment pipelines.", icon: "database", categories: ["mlops-sim2real", "mlops-data-deployment"] },
  { slug: "geometry", title: "Geometry, calibration & SLAM", description: "Work with coordinate frames, camera calibration, mapping, and state estimation.", icon: "axis", categories: ["geometry-calibration-slam"] },
  { slug: "control", title: "Planning, control & kinematics", description: "Turn goals into feasible paths, joint configurations, and feedback controls.", icon: "route", categories: ["planning-control-ik"] },
  { slug: "robot-learning", title: "Robot learning & reinforcement learning", description: "Study policy updates, imitation, rewards, and learning from robot experience.", icon: "brain", categories: ["robot-learning-rl"] },
  { slug: "vlm", title: "Vision-language grounding", description: "Connect images, language, and spatial concepts for embodied reasoning.", icon: "eye", categories: ["vlm-grounding"] },
  { slug: "manipulation", title: "Manipulation, humanoids & touch", description: "Explore contact, dexterous hands, bimanual actions, and whole-body coordination.", icon: "hand", categories: ["humanoid-dexterity-tactile"] },
  { slug: "simulation", title: "Simulation & sim-to-real", description: "Study simulated environments, domain randomization, and transfer to physical robots.", icon: "boxes", categories: ["simulation-sim2real"] },
] as const;

export function projectSheet(category: string) {
  return projectSheets.find(sheet => (sheet.categories as readonly string[]).includes(category));
}

export function findProject(papers: Paper[], id: string) {
  return papers.find(paper => paper.id === id || paper.aliases?.includes(id));
}

export function linkedProjectProblems(paper: Paper, problems: ProblemMeta[]) {
  const slugs = new Set([...paper.problemSlugs, ...(paper.executionFlow?.nodes.flatMap(node => node.problem_slugs) || [])]);
  return problems.filter(problem => slugs.has(problem.slug));
}

export type ProjectSummary = ReturnType<typeof summarizeProject>;
export function summarizeProject(paper: Paper, problems: ProblemMeta[]) {
  const linked = linkedProjectProblems(paper, problems);
  return {
    id: paper.id, title: paper.title, year: paper.year, authors: paper.authors.join(", "),
    topics: paper.topics, sheet: projectSheet(paper.category)?.slug || "", stages: paper.executionFlow?.nodes.length || 0,
    description: paper.executionFlow?.description || "Source paper collected. The guided explanation, model flow, and implementation steps are being prepared.",
    problems: linked.map(({ slug, title, difficulty }) => ({ slug, title, difficulty })),
  };
}
