export type ProblemMeta = {
  slug: string; title: string; version: string; number: number;
  difficulty: "Easy" | "Medium" | "Hard"; domain: string; topics: string[];
  minutes: number; framework: string; entrypoint: string; paperIds: string[];
  prerequisites: string[]; visualization: string; summary: string;
};
export type Problem = ProblemMeta & { problem: string; theory: string; starter: string; solution: string; reference: string };
export type PaperFlowNode = { id: string; title: string; detail: string; column: number; row: number; section: string; problem_slugs: string[]; planned_problems?: string[] };
export type PaperFlow = { title: string; description: string; nodes: PaperFlowNode[]; edges: { from: string; to: string; label: string }[] };
export type Paper = { id: string; aliases?: string[]; title: string; year: number; authors: string[]; topics: string[]; primaryUrl: string; category: string; brief: string; content: string; problemSlugs: string[]; executionFlow?: PaperFlow };
export type Track = { slug: string; title: string; subtitle: string; description: string; icon: string; color: string; slugs: string[]; objectives: string[] };
export type TestResult = { name: string; passed: boolean; message?: string; visibility: string; duration_ms?: number };
export type RobotPreview = { kind: "fr3-joint-trajectory-v1"; q: number[][] };
export type Job = { preview?: RobotPreview; preview_error?: string; id: string; slug: string; mode: "run" | "submit"; status: "queued" | "running" | "completed" | "failed"; created_at: string; code: string; tests?: TestResult[]; passed?: boolean; error?: string; logs?: string; duration_ms?: number; lineage?: Record<string,string|number>; };
