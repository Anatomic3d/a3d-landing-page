import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

const rootArg = process.argv[2] ?? ".";
const port = Number(process.env.PORT ?? 3000);
const root = path.resolve(process.cwd(), rootArg);

const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json",
  ".webp": "image/webp"
};

function safePathFromUrl(url) {
  const requestPath = decodeURIComponent(new URL(url, "http://localhost").pathname);
  const normalizedPath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, "");
  const filePath = path.join(root, normalizedPath);

  if (!filePath.startsWith(root)) {
    return null;
  }

  return filePath;
}

async function resolveFile(url) {
  const filePath = safePathFromUrl(url);
  if (!filePath) return null;

  try {
    const stats = await stat(filePath);
    if (stats.isDirectory()) return path.join(filePath, "index.html");
    if (stats.isFile()) return filePath;
  } catch {
    return path.join(root, "index.html");
  }

  return null;
}

const server = createServer(async (req, res) => {
  const filePath = await resolveFile(req.url ?? "/");

  if (!filePath) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }

  try {
    const stats = await stat(filePath);
    if (!stats.isFile()) throw new Error("Not a file");

    res.writeHead(200, {
      "Content-Length": stats.size,
      "Content-Type": contentTypes[path.extname(filePath).toLowerCase()] ?? "application/octet-stream",
      "X-Content-Type-Options": "nosniff"
    });
    createReadStream(filePath).pipe(res);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});

server.listen(port, () => {
  const script = path.relative(process.cwd(), fileURLToPath(import.meta.url));
  console.log(`${script} serving ${root} at http://localhost:${port}`);
});
