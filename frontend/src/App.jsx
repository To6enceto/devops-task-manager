import { useState, useEffect, useCallback } from "react";
import TaskCard from "./components/TaskCard";
import TaskForm from "./components/TaskForm";
import "./App.css";

const API = "/api/tasks";
const STATUSES = ["all", "pending", "in_progress", "done"];
const STATUS_LABELS = { all: "All", pending: "Pending", in_progress: "In Progress", done: "Done" };

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editTask, setEditTask] = useState(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const url = filter === "all" ? API : `${API}?status=${filter}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to fetch tasks");
      setTasks(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { fetchTasks(); }, [fetchTasks]);

  const handleCreate = async (data) => {
    const res = await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create task");
    setShowForm(false);
    fetchTasks();
  };

  const handleUpdate = async (id, data) => {
    const res = await fetch(`${API}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to update task");
    setEditTask(null);
    fetchTasks();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this task?")) return;
    const res = await fetch(`${API}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete task");
    fetchTasks();
  };

  const counts = tasks.reduce(
    (acc, t) => { acc[t.status] = (acc[t.status] || 0) + 1; return acc; },
    {}
  );

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="header-title">
            <span className="header-logo">✅</span>
            <div>
              <h1>DevOps Task Manager</h1>
              <span className="header-sub">Full-stack app deployed on Kubernetes</span>
            </div>
          </div>
          <button className="btn-primary" onClick={() => { setEditTask(null); setShowForm(true); }}>
            + New Task
          </button>
        </div>
      </header>

      {/* Stats bar */}
      <div className="stats-bar">
        <div className="stat"><span className="stat-num">{tasks.length}</span><span className="stat-label">Total</span></div>
        <div className="stat"><span className="stat-num" style={{ color: "var(--yellow)" }}>{counts.pending || 0}</span><span className="stat-label">Pending</span></div>
        <div className="stat"><span className="stat-num" style={{ color: "var(--accent)" }}>{counts.in_progress || 0}</span><span className="stat-label">In Progress</span></div>
        <div className="stat"><span className="stat-num" style={{ color: "var(--green)" }}>{counts.done || 0}</span><span className="stat-label">Done</span></div>
      </div>

      {/* Modal */}
      {(showForm || editTask) && (
        <div className="modal-overlay" onClick={() => { setShowForm(false); setEditTask(null); }}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editTask ? "Edit Task" : "New Task"}</h2>
              <button className="btn-ghost" onClick={() => { setShowForm(false); setEditTask(null); }}>✕</button>
            </div>
            <TaskForm
              initial={editTask}
              onSubmit={editTask ? (d) => handleUpdate(editTask.id, d) : handleCreate}
              onCancel={() => { setShowForm(false); setEditTask(null); }}
            />
          </div>
        </div>
      )}

      {/* Main */}
      <main className="main">
        {/* Filter tabs */}
        <div className="filter-tabs">
          {STATUSES.map((s) => (
            <button
              key={s}
              className={`tab ${filter === s ? "tab-active" : ""}`}
              onClick={() => setFilter(s)}
            >
              {STATUS_LABELS[s]}
              {s !== "all" && counts[s] ? <span className="tab-badge">{counts[s]}</span> : null}
            </button>
          ))}
        </div>

        {/* Task grid */}
        {error && <div className="error-banner">⚠ {error} <button className="btn-ghost" onClick={fetchTasks}>Retry</button></div>}
        {loading ? (
          <div className="empty-state"><div className="spinner" /></div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📋</span>
            <p>{filter === "all" ? "No tasks yet. Create your first one!" : `No ${STATUS_LABELS[filter].toLowerCase()} tasks.`}</p>
          </div>
        ) : (
          <div className="task-grid">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => setEditTask(task)}
                onDelete={() => handleDelete(task.id)}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
