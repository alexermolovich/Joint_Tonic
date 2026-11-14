import type { NextConfig } from "next";
import path from "node:path";

const config: NextConfig = {
  devIndicators: false,
  turbopack: { root: path.resolve(__dirname, "../..") },
  serverExternalPackages: ["gray-matter"],
};
export default config;
