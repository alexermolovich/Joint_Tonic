export type WorkspaceItem = { kind: "draft" | "note" | "bookmark"; slug: string; version: string; body: string; revision: number };
export type WorkspaceChange = Omit<WorkspaceItem, "revision"> & { expectedRevision: number };
export function itemKey(item: Pick<WorkspaceItem, "kind" | "slug" | "version">) { return `${item.kind}:${item.slug}@${item.version}`; }
export function parseWorkspaceChange(value: unknown): WorkspaceChange {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("Invalid workspace change.");
  const v = value as Record<string, unknown>;
  if (Object.keys(v).sort().join(",") !== "body,expectedRevision,kind,slug,version" || !["draft", "note", "bookmark"].includes(String(v.kind)) || typeof v.slug !== "string" || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(v.slug) || v.slug.length > 160 || typeof v.version !== "string" || !/^\d+\.\d+\.\d+$/.test(v.version) || typeof v.body !== "string" || new TextEncoder().encode(v.body).length > 100000 || !Number.isSafeInteger(v.expectedRevision) || Number(v.expectedRevision) < 0 || (v.kind === "bookmark" && v.body !== "0" && v.body !== "1")) throw new Error("Invalid workspace change.");
  return v as unknown as WorkspaceChange;
}
