const express = require("express");
const cors = require("cors");
const path = require("path");
const client = require("prom-client");
const { initDb, pool } = require("./db");
const tasksRouter = require("./routes/tasks");

const app = express();
const PORT = parseInt(process.env.PORT || "8000");
const APP_NAME = process.env.APP_NAME || "DevOps Task Manager";
const APP_VERSION = process.env.APP_VERSION || "1.0.0";

// ── Prometheus metrics ──────────────────────────────────────────────────────
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequestCounter = new client.Counter({
  name: "http_requests_total",
  help: "Total HTTP request count",
  labelNames: ["method", "path", "status"],
  registers: [register],
});

const httpRequestDuration = new client.Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request duration in seconds",
  labelNames: ["method", "path", "status"],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [register],
});

// ── Middleware ───────────────────────────────────────────────────────────────
app.use(cors());
app.use(express.json());

// Metrics middleware
app.use((req, res, next) => {
  if (req.path === "/metrics") return next();
  const end = httpRequestDuration.startTimer({ method: req.method, path: req.path });
  res.on("finish", () => {
    const labels = { method: req.method, path: req.path, status: res.statusCode };
    httpRequestCounter.inc(labels);
    end({ ...labels });
  });
  next();
});

// ── Health & info endpoints ──────────────────────────────────────────────────
// ── Health & info endpoints ──────────────────────────────────────────────────
app.get("/api/info", (req, res) => {
  res.json({ app: APP_NAME, version: APP_VERSION, docs: "/api/tasks" });
});

app.get("/health", (req, res) => {
  res.json({ status: "healthy" });
});

app.get("/ready", async (req, res) => {
  try {
    await pool.query("SELECT 1");
    res.json({ status: "ready" });
  } catch {
    res.status(503).json({ status: "not ready" });
  }
});

app.get("/metrics", async (req, res) => {
  res.setHeader("Content-Type", register.contentType);
  res.send(await register.metrics());
});

// ── API routes ───────────────────────────────────────────────────────────────
app.use("/api/tasks", tasksRouter);
// Keep /tasks for backward compat with existing k8s probes / ArgoCD
app.use("/tasks", tasksRouter);

// ── Serve React frontend ─────────────────────────────────────────────────────
const staticDir = path.join(__dirname, "public");
app.use(express.static(staticDir));
app.get("*", (req, res) => {
  res.sendFile(path.join(staticDir, "index.html"));
});

// ── Error handler ────────────────────────────────────────────────────────────
app.use((err, req, res, _next) => {
  console.error(JSON.stringify({ level: "error", message: err.message, path: req.path }));
  res.status(500).json({ detail: "Internal server error" });
});

// ── Start ────────────────────────────────────────────────────────────────────
let server;
async function start() {
  await initDb();
  server = app.listen(PORT, "0.0.0.0", () => {
    console.log(JSON.stringify({ level: "info", message: `${APP_NAME} v${APP_VERSION} listening on :${PORT}` }));
  });
}

process.on("SIGTERM", () => {
  server?.close(() => {
    pool.end();
    process.exit(0);
  });
});

if (process.env.NODE_ENV !== "test") {
  start().catch((err) => {
    console.error(JSON.stringify({ level: "error", message: err.message }));
    process.exit(1);
  });
}

module.exports = app;

module.exports = app; // for tests
