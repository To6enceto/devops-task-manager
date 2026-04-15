const request = require("supertest");

// Mock the db module so tests don't need a real DB
jest.mock("../db", () => {
  const tasks = [
    { id: 1, title: "Test task", description: "desc", status: "pending", created_at: new Date(), updated_at: new Date() },
  ];
  return {
    pool: {
      query: jest.fn(async (sql, params) => {
        if (sql.includes("SELECT 1")) return { rows: [{ "?column?": 1 }], rowCount: 1 };
        if (sql.includes("SELECT * FROM tasks WHERE id")) {
          const id = parseInt(params[0]);
          const row = tasks.find((t) => t.id === id);
          return { rows: row ? [row] : [], rowCount: row ? 1 : 0 };
        }
        if (sql.includes("SELECT * FROM tasks") || sql.startsWith("SELECT * FROM tasks")) {
          return { rows: tasks, rowCount: tasks.length };
        }
        if (sql.includes("INSERT")) {
          const newTask = { id: 2, title: params[0], description: params[1], status: params[2], created_at: new Date(), updated_at: new Date() };
          tasks.push(newTask);
          return { rows: [newTask], rowCount: 1 };
        }
        if (sql.includes("UPDATE")) {
          const id = parseInt(params[3]);
          const t = tasks.find((t) => t.id === id);
          if (!t) return { rows: [], rowCount: 0 };
          Object.assign(t, { title: params[0], description: params[1], status: params[2], updated_at: new Date() });
          return { rows: [t], rowCount: 1 };
        }
        if (sql.includes("DELETE")) {
          const id = parseInt(params[0]);
          const idx = tasks.findIndex((t) => t.id === id);
          if (idx === -1) return { rows: [], rowCount: 0 };
          tasks.splice(idx, 1);
          return { rows: [{ id }], rowCount: 1 };
        }
        return { rows: [], rowCount: 0 };
      }),
      end: jest.fn(),
    },
    initDb: jest.fn(async () => {}),
  };
});

const app = require("../index");

describe("Health endpoints", () => {
  it("GET / returns app info", async () => {
    const res = await request(app).get("/");
    expect(res.status).toBe(200);
    expect(res.body.app).toBeDefined();
  });

  it("GET /health returns healthy", async () => {
    const res = await request(app).get("/health");
    expect(res.status).toBe(200);
    expect(res.body.status).toBe("healthy");
  });

  it("GET /ready returns ready", async () => {
    const res = await request(app).get("/ready");
    expect(res.status).toBe(200);
  });
});

describe("Tasks CRUD", () => {
  it("GET /api/tasks returns list", async () => {
    const res = await request(app).get("/api/tasks");
    expect(res.status).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it("POST /api/tasks creates a task", async () => {
    const res = await request(app)
      .post("/api/tasks")
      .send({ title: "New task", description: "Test", status: "pending" });
    expect(res.status).toBe(201);
    expect(res.body.title).toBe("New task");
  });

  it("POST /api/tasks without title returns 422", async () => {
    const res = await request(app).post("/api/tasks").send({});
    expect(res.status).toBe(422);
  });

  it("GET /api/tasks/:id returns task", async () => {
    const res = await request(app).get("/api/tasks/1");
    expect(res.status).toBe(200);
    expect(res.body.id).toBe(1);
  });

  it("GET /api/tasks/:id not found returns 404", async () => {
    const res = await request(app).get("/api/tasks/9999");
    expect(res.status).toBe(404);
  });

  it("PUT /api/tasks/:id updates task", async () => {
    const res = await request(app)
      .put("/api/tasks/1")
      .send({ title: "Updated", status: "in_progress" });
    expect(res.status).toBe(200);
    expect(res.body.title).toBe("Updated");
  });

  it("DELETE /api/tasks/:id deletes task", async () => {
    const res = await request(app).delete("/api/tasks/1");
    expect(res.status).toBe(204);
  });

  it("DELETE /api/tasks/:id not found returns 404", async () => {
    const res = await request(app).delete("/api/tasks/9999");
    expect(res.status).toBe(404);
  });
});
