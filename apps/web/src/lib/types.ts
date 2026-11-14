export type ProblemMeta = {
  slug: string; title: string; version: string; number: number;
  difficulty: "Easy" | "Medium" | "Hard"; domain: string; topics: string[];
  minutes: number; framework: string; entrypoint: string; paperIds: string[];
  prerequisites: string[]; visualization: string; summary: string;
};
export type Problem = ProblemMeta & { problem: string; theory: string; starter: string; solution: string; reference: string };
export type Paper = { id: string; title: string; year: number; authors: string[]; topics: string[]; primaryUrl: string; category: string; brief: string; content: string; problemSlugs: string[] };
export type Track = { slug: string; title: string; subtitle: string; description: string; icon: string; color: string; slugs: string[]; objectives: string[] };
export type TestResult = { name: string; passed: boolean; message?: string; visibility: string; duration_ms?: number };
export type Job = { id: string; slug: string; mode: "run" | "submit"; status: "queued" | "running" | "completed" | "failed"; created_at: string; code: string; tests?: TestResult[]; passed?: boolean; error?: string; logs?: string; duration_ms?: number; lineage?: Record<string,string|number>; };
