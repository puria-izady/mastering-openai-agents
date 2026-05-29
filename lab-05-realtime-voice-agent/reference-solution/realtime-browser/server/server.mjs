import express from "express";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { buildClientSecretRequest } from "./session-config.mjs";

const app = express();
const port = Number(process.env.PORT ?? 8787);
const __dirname = fileURLToPath(new URL(".", import.meta.url));
const distDir = join(__dirname, "../dist");

app.get("/token", async (_req, res) => {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    res.status(401).json({
      error: "OPENAI_API_KEY is required on the trusted server to mint a realtime client secret."
    });
    return;
  }

  const request = buildClientSecretRequest(apiKey);
  const response = await fetch(request.url, request.init);
  const text = await response.text();

  res.status(response.status).type(response.headers.get("content-type") ?? "application/json");
  res.send(text);
});

if (existsSync(distDir)) {
  app.use(express.static(distDir));
  app.get("*", (_req, res) => res.sendFile(join(distDir, "index.html")));
}

app.listen(port, () => {
  console.log(`Realtime token server listening on http://127.0.0.1:${port}`);
});
