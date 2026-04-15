import "./TaskCard.css";

const STATUS_CONFIG = {
  pending:     { label: "Pending",     color: "#d29922", bg: "rgba(210,153,34,0.12)" },
  in_progress: { label: "In Progress", color: "#58a6ff", bg: "rgba(88,166,255,0.12)" },
  done:        { label: "Done",        color: "#3fb950", bg: "rgba(63,185,80,0.12)" },
};

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
}

export default function TaskCard({ task, onEdit, onDelete }) {
  const cfg = STATUS_CONFIG[task.status] || STATUS_CONFIG.pending;

  return (
    <div className="task-card">
      <div className="task-card-header">
        <span className="task-badge" style={{ color: cfg.color, background: cfg.bg }}>
          {cfg.label}
        </span>
        <span className="task-id">#{task.id}</span>
      </div>

      <h3 className="task-title">{task.title}</h3>

      {task.description && (
        <p className="task-desc">{task.description}</p>
      )}

      <div className="task-footer">
        <span className="task-date">{formatDate(task.created_at)}</span>
        <div className="task-actions">
          <button className="btn-ghost btn-sm" onClick={onEdit} title="Edit">✏️</button>
          <button className="btn-ghost btn-sm" onClick={onDelete} title="Delete" style={{ color: "var(--red)" }}>🗑️</button>
        </div>
      </div>
    </div>
  );
}
