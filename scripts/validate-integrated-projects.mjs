import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const problems = new Set(fs.readdirSync(path.join(root, "content/problems")));
const paperIds = new Set();
for (const topic of fs.readdirSync(path.join(root, "research/papers"), { withFileTypes: true })) {
  if (!topic.isDirectory()) continue;
  for (const name of fs.readdirSync(path.join(root, "research/papers", topic.name))) if (name.endsWith(".md")) paperIds.add(name.slice(0, -3));
}
const failures = [];
let count = 0;
for (const folder of ["capstones", "paper-projects"]) {
  const base = path.join(root, "content", folder);
  if (!fs.existsSync(base)) continue;
  for (const entry of fs.readdirSync(base, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const label = `${folder}/${entry.name}`;
    try {
      const directory = path.join(base, entry.name);
      const project = JSON.parse(fs.readFileSync(path.join(directory, "meta.json"), "utf8"));
      if (project.slug !== entry.name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(project.slug)) throw new Error("invalid slug");
      if (![project.title, project.summary].every(value => typeof value === "string" && value.trim())) throw new Error("missing title/summary");
      if (!/^\d+\.\d+\.\d+$/.test(project.version)) throw new Error("invalid semantic version");
      if (!problems.has(project.integrationProblemSlug)) throw new Error("integration problem is not published");
      if (!Array.isArray(project.paperIds) || !project.paperIds.length || project.paperIds.some(id => !paperIds.has(id))) throw new Error("unknown source paper");
      if (!Array.isArray(project.stages) || !project.stages.length) throw new Error("missing stages");
      for (const stage of project.stages) {
        if (![stage.title, stage.description].every(value => typeof value === "string" && value.trim())) throw new Error("stage description missing");
        if (!Array.isArray(stage.problemSlugs) || stage.problemSlugs.some(slug => !problems.has(slug))) throw new Error("unknown component problem");
      }
      for (const name of ["orientation", "evaluation", "reproducibility"]) {
        const text = fs.readFileSync(path.join(directory, `${name}.md`), "utf8");
        if (!text.trim()) throw new Error(`${name} is empty`);
        for (const match of text.matchAll(/\]\(\/problems\/([a-z0-9-]+)\)/g)) if (!problems.has(match[1])) throw new Error(`unknown problem link ${match[1]}`);
      }
      count++;
    } catch (error) { failures.push(`${label}: ${error.message}`); }
  }
}
console.log(JSON.stringify({ projects: count, failures }, null, 2));
if (failures.length) process.exitCode = 1;
