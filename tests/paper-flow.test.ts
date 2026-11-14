import test from "node:test";
import assert from "node:assert/strict";
import { parsePaperFlow, paperSectionId } from "../apps/web/src/lib/paper-flow.ts";

const markdown = "## Input contract\n\n## Forward diffusion\n";
const flow = {
  title: "Action training", description: "Inputs become noisy actions.",
  nodes: [
    { id: "input", title: "Actions", detail: "Clean batch", column: 0, row: 0, section: "Input contract", problem_slugs: [] },
    { id: "noise", title: "Add noise", detail: "Known noise and schedule", column: 1, row: 0, section: "Forward diffusion", problem_slugs: ["diffusion-action-noising"] },
  ],
  edges: [{ from: "input", to: "noise", label: "A0 (B,H,D)" }],
};
test("valid flow retains runnable links and stable article anchors", () => {
  assert.deepEqual(parsePaperFlow(flow, markdown, ["diffusion-action-noising"]), flow);
  assert.equal(paperSectionId("Forward diffusion"), "paper-section-forward-diffusion");
  assert.equal(parsePaperFlow(undefined, markdown, []), undefined);
});
test("rejects dangling sections, problem routes, and graph edges", () => {
  assert.throws(() => parsePaperFlow(flow, "## Input contract\n", ["diffusion-action-noising"]), /Missing flow section/);
  assert.throws(() => parsePaperFlow(flow, markdown, []), /Unknown flow problem/);
  assert.throws(() => parsePaperFlow({ ...flow, edges: [{ from: "input", to: "missing", label: "x" }] }, markdown, ["diffusion-action-noising"]), /Invalid flow edge/);
});
test("rejects overlapping nodes and unbounded coordinates", () => {
  assert.throws(() => parsePaperFlow({ ...flow, nodes: [flow.nodes[0], { ...flow.nodes[1], column: 0 }] }, markdown, ["diffusion-action-noising"]), /Duplicate or invalid/);
  assert.throws(() => parsePaperFlow({ ...flow, nodes: [flow.nodes[0], { ...flow.nodes[1], row: 100 }] }, markdown, ["diffusion-action-noising"]), /Invalid flow position/);
});

test("planned exercises remain non-runnable until an exact published title resolves", () => {
  const candidate = { ...flow, nodes: [flow.nodes[0], { ...flow.nodes[1], planned_problems: ["Add Noise to an Action Sequence", "Train a denoiser", "Train a denoiser"] }] };
  const pending = parsePaperFlow(candidate, markdown, ["diffusion-action-noising"]);
  assert.deepEqual(pending?.nodes[1].planned_problems, ["Add Noise to an Action Sequence", "Train a denoiser"]);
  const resolved = parsePaperFlow(candidate, markdown, ["diffusion-action-noising"], [{ slug: "diffusion-action-noising", title: "Add Noise to an Action Sequence" }]);
  assert.deepEqual(resolved?.nodes[1].problem_slugs, ["diffusion-action-noising"]);
  assert.deepEqual(resolved?.nodes[1].planned_problems, ["Train a denoiser"]);
});

test("similar or ambiguous titles cannot silently become runnable links", () => {
  const candidate = { ...flow, nodes: [{ ...flow.nodes[0], planned_problems: ["Train a policy", "Action noise"] }, flow.nodes[1]] };
  const resolved = parsePaperFlow(candidate, markdown, ["diffusion-action-noising", "a", "b"], [{ slug: "a", title: "Train a policy" }, { slug: "b", title: "Train a policy" }, { slug: "diffusion-action-noising", title: "Add action noise" }]);
  assert.deepEqual(resolved?.nodes[0].problem_slugs, []);
  assert.deepEqual(resolved?.nodes[0].planned_problems, ["Train a policy", "Action noise"]);
});

test("planned titles are bounded data, never arbitrary links or objects", () => {
  for (const planned_problems of [[""], [null], [{ title: "Oops" }], Array(13).fill("Task"), ["x".repeat(201)], "Task"]) {
    assert.throws(() => parsePaperFlow({ ...flow, nodes: [{ ...flow.nodes[0], planned_problems }, flow.nodes[1]] }, markdown, ["diffusion-action-noising"]));
  }
});
