import test from "node:test";
import assert from "node:assert/strict";
import { findProject, linkedProjectProblems, projectSheets, projectSheet, summarizeProject } from "../apps/web/src/lib/projects.ts";
import type { Paper, ProblemMeta } from "../apps/web/src/lib/types.ts";

const problems = [
  { slug: "direct", title: "Direct component", difficulty: "Easy" },
  { slug: "flow", title: "Flow component", difficulty: "Medium" },
] as ProblemMeta[];
const paper: Paper = {
  id: "canonical", aliases: ["alternate"], title: "A robot paper", year: 2024, authors: ["A. Author"],
  topics: ["robotics"], primaryUrl: "https://example.com/paper", category: "vla-embodied", brief: "", content: "",
  problemSlugs: ["direct", "direct", "missing"], executionFlow: {
    title: "Model", description: "A grounded model flow.", nodes: [
      { id: "step", title: "Step", detail: "Transform input", column: 0, row: 0, section: "Step", problem_slugs: ["flow", "direct"] },
    ], edges: [],
  },
};

test("project availability counts unique existing problems from direct and stage associations", () => {
  assert.deepEqual(linkedProjectProblems(paper, problems).map(problem => problem.slug), ["direct", "flow"]);
  const summary = summarizeProject(paper, problems);
  assert.equal(summary.problems.length, 2);
  assert.equal(summary.stages, 1);
  assert.equal(summary.sheet, "vla");
  assert.equal(summarizeProject({ ...paper, executionFlow: undefined }, problems).stages, 0);
});

test("alternate paper IDs resolve to the same canonical project and unknown IDs stay missing", () => {
  assert.equal(findProject([paper], "alternate"), paper);
  assert.equal(findProject([paper], "canonical"), paper);
  assert.equal(findProject([paper], "unknown"), undefined);
});

test("every source folder maps to one topic sheet", () => {
  const folders = projectSheets.flatMap(sheet => [...sheet.categories]);
  assert.equal(folders.length, 12);
  assert.equal(new Set(folders).size, folders.length);
  assert.equal(projectSheet("mlops-data-deployment")?.slug, "mlops");
  assert.equal(projectSheet("not-a-folder"), undefined);
});
