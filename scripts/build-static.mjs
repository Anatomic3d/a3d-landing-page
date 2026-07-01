import { cp, mkdir, readdir, rm } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const outDir = path.join(root, "dist");
const copiedExtensions = new Set([
  ".html",
  ".css",
  ".js",
  ".mjs",
  ".png",
  ".jpg",
  ".jpeg",
  ".gif",
  ".glb",
  ".webp",
  ".svg",
  ".ico",
  ".json",
  ".txt",
  ".webmanifest"
]);

const ignoredNames = new Set([
  ".agents",
  ".codex",
  ".git",
  "dist",
  "node_modules",
  "package-lock.json",
  "package.json",
  "scripts",
  "vercel.json"
]);

async function copyStaticFiles(fromDir, toDir) {
  const entries = await readdir(fromDir, { withFileTypes: true });

  for (const entry of entries) {
    if (ignoredNames.has(entry.name)) continue;

    const source = path.join(fromDir, entry.name);
    const target = path.join(toDir, entry.name);

    if (entry.isDirectory()) {
      await copyStaticFiles(source, target);
      continue;
    }

    if (entry.isFile() && copiedExtensions.has(path.extname(entry.name).toLowerCase())) {
      await mkdir(path.dirname(target), { recursive: true });
      await cp(source, target);
    }
  }
}

await rm(outDir, { recursive: true, force: true });
await mkdir(outDir, { recursive: true });
await copyStaticFiles(root, outDir);

console.log(`Static site built at ${path.relative(root, outDir)}`);
