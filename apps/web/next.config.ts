import type { NextConfig } from "next";
import path from "node:path";

const config: NextConfig = {
  devIndicators: false,
  turbopack: { root: path.resolve(__dirname, "../..") },
  outputFileTracingRoot: path.resolve(__dirname, "../.."),
  outputFileTracingIncludes: {
    "/*": [
      "../../SPEC.md",
      "../../content/problems/*/meta.json",
      "../../content/problems/*/{problem,theory,solution}.md",
      "../../content/problems/*/{starter,reference}.py",
      "../../content/tracks/papers/*.md",
      "../../research/papers/**/*.md",
    ],
  },
  outputFileTracingExcludes: {
    "/*": ["../../.local/**/*", "../../research/papers/**/*.pdf", "../../content/problems/*/cases.py"],
  },
  serverExternalPackages: ["gray-matter"],
};
export default config;
