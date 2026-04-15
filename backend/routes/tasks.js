const express = require("express");
const router = express.Router();
const { pool } = require("../db");

// GET /tasks
router.get("/", async (req, res) => {
  const { status } = req.query;
  const params = [];
  let query = "SELECT * FROM tasks";
  if (status) {
    query += " WHERE status = $1";
    params.push(status);
  }
  query += " ORDER BY created_at DESC";
  const result = await pool.query(query, params);
  res.json(result.rows);
});

// GET /tasks/:id
router.get("/:id", async (req, res) => {
  const result = await pool.query("SELECT * FROM tasks WHERE id = $1", [req.params.id]);
  if (result.rowCount === 0) return res.status(404).json({ detail: "Task not found" });
  res.json(result.rows[0]);
});

// POST /tasks
router.post("/", async (req, res) => {
  const { title, description, status = "pending" } = req.body;
  if (!title) return res.status(422).json({ detail: "title is required" });
  const result = await pool.query(
    "INSERT INTO tasks (title, description, status) VALUES ($1, $2, $3) RETURNING *",
    [title, description || null, status]
  );
  res.status(201).json(result.rows[0]);
});

// PUT /tasks/:id
router.put("/:id", async (req, res) => {
  const { title, description, status } = req.body;
  const existing = await pool.query("SELECT * FROM tasks WHERE id = $1", [req.params.id]);
  if (existing.rowCount === 0) return res.status(404).json({ detail: "Task not found" });

  const current = existing.rows[0];
  const result = await pool.query(
    `UPDATE tasks SET
      title = $1,
      description = $2,
      status = $3,
      updated_at = NOW()
     WHERE id = $4 RETURNING *`,
    [
      title ?? current.title,
      description !== undefined ? description : current.description,
      status ?? current.status,
      req.params.id,
    ]
  );
  res.json(result.rows[0]);
});

// DELETE /tasks/:id
router.delete("/:id", async (req, res) => {
  const result = await pool.query("DELETE FROM tasks WHERE id = $1 RETURNING id", [req.params.id]);
  if (result.rowCount === 0) return res.status(404).json({ detail: "Task not found" });
  res.status(204).send();
});

module.exports = router;
