"""Generate architecture diagram PNG for the DevOps Task Manager project."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(20, 13))
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)
ax.axis("off")
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")

# Colors
C_BG = "#0d1117"
C_BORDER = "#30363d"
C_DEV = "#1f3a4f"
C_GITHUB = "#1a2332"
C_DOCKER = "#1a2d3a"
C_K8S = "#1a2a1a"
C_MONITOR = "#2a1a2a"
C_TEXT = "#e6edf3"
C_SUBTEXT = "#8b949e"
C_ARROW = "#58a6ff"
C_YELLOW = "#d29922"
C_GREEN = "#3fb950"
C_PURPLE = "#bc8cff"
C_ORANGE = "#f78166"
C_BLUE = "#58a6ff"

def box(ax, x, y, w, h, color, label, sublabel=None, text_color=C_TEXT, fontsize=9, border_color=None):
    bc = border_color or color
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor=bc, linewidth=1.5)
    ax.add_patch(rect)
    ty = y + h / 2 + (0.15 if sublabel else 0)
    ax.text(x + w/2, ty, label, ha="center", va="center",
            color=text_color, fontsize=fontsize, fontweight="bold")
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.2, sublabel, ha="center", va="center",
                color=C_SUBTEXT, fontsize=7)

def group(ax, x, y, w, h, color, title):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=color, edgecolor=C_BORDER, linewidth=2, linestyle="--")
    ax.add_patch(rect)
    ax.text(x + 0.2, y + h - 0.05, title, ha="left", va="top",
            color=C_SUBTEXT, fontsize=8, fontstyle="italic")

def arrow(ax, x1, y1, x2, y2, color=C_ARROW, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.1, label, ha="center", va="bottom",
                color=color, fontsize=6.5)

# ── Title ──────────────────────────────────────────────────────────────────
ax.text(10, 12.6, "DevOps Task Manager — Architecture", ha="center", va="center",
        color=C_TEXT, fontsize=14, fontweight="bold")

# ── DEVELOPER (col 0) ──────────────────────────────────────────────────────
group(ax, 0.2, 9.5, 2.8, 2.8, C_DEV, "Developer")
box(ax, 0.5, 11.0, 2.2, 0.9, "#21384f", "Developer", "git commit", fontsize=8)
box(ax, 0.5, 9.8, 2.2, 0.9, "#21384f", "Pre-commit Hooks",
    "black · flake8 · bandit\ngitleaks · detect-key", fontsize=7.5)

# ── GITHUB CI (col 1-2) ────────────────────────────────────────────────────
group(ax, 3.3, 8.0, 5.4, 4.6, C_GITHUB, "GitHub Actions CI")
box(ax, 3.6, 11.2, 2.4, 1.0, "#21324a", "Lint & Security",
    "pre-commit hooks", fontsize=8)
box(ax, 6.0, 11.2, 2.4, 1.0, "#21324a", "Tests + Coverage",
    "pytest · 70% min", fontsize=8)
box(ax, 3.6, 9.8, 2.4, 1.0, "#21324a", "Build & Push",
    "Docker image", fontsize=8)
box(ax, 6.0, 9.8, 2.4, 1.0, "#21324a", "Update Manifests",
    "k8s/overlays/prod", fontsize=8)
box(ax, 4.8, 8.4, 2.4, 1.0, "#21324a", "Discord Notify",
    "CI status webhook", fontsize=8)

# ── DOCKER HUB (col 3) ─────────────────────────────────────────────────────
group(ax, 9.0, 9.5, 2.8, 2.8, C_DOCKER, "Docker Hub")
box(ax, 9.3, 10.7, 2.2, 0.9, "#1a3040", "task-manager", "sha-xxxxx · latest", fontsize=8)
box(ax, 9.3, 9.7, 2.2, 0.8, "#1a3040", "to6eto/", "Docker Hub registry", fontsize=7.5)

# ── KUBERNETES CLUSTER ─────────────────────────────────────────────────────
group(ax, 0.2, 0.3, 11.6, 8.9, "#111a11", "DOKS Kubernetes Cluster  (Terraform IaC)")

# ArgoCD
group(ax, 0.5, 6.8, 3.0, 2.0, "#1a2a1a", "argocd ns")
box(ax, 0.7, 7.2, 2.6, 1.3, "#22382a", "ArgoCD",
    "GitOps CD\nauto-sync + self-heal", fontsize=8)

# task-manager namespace
group(ax, 3.7, 4.8, 5.0, 4.0, "#1a2a1a", "task-manager ns")
box(ax, 3.9, 7.2, 2.2, 1.3, "#22382a", "FastAPI App",
    "3 replicas\nHPA: 2–10", fontsize=8)
box(ax, 6.3, 7.2, 2.2, 1.3, "#22382a", "PostgreSQL",
    "StatefulSet\nPersistentVolume", fontsize=8)
box(ax, 3.9, 5.2, 2.2, 1.6, "#22382a", "Sealed Secret",
    "DATABASE_URL\n(encrypted in Git)", fontsize=7.5)
box(ax, 6.3, 5.2, 2.2, 1.6, "#22382a", "ConfigMap + Ingress",
    "nginx ingress\nhttp://188.166.x.x", fontsize=7.5)

# kube-system
group(ax, 0.5, 4.8, 3.0, 1.7, "#1a2a1a", "kube-system")
box(ax, 0.7, 5.2, 2.6, 1.0, "#22382a", "Sealed Secrets Ctrl\n+ Ingress NGINX",
    "bitnami controller", fontsize=7.5)

# monitoring namespace
group(ax, 0.5, 0.6, 11.0, 3.9, "#2a1a2a", "monitoring ns")
box(ax, 0.7, 1.0, 2.4, 2.7, "#3a1a3a", "Prometheus",
    "metrics scrape\n/metrics endpoint\nalerts evaluation", fontsize=7.5)
box(ax, 3.3, 1.0, 2.4, 2.7, "#3a1a3a", "Grafana",
    "dashboards\nTask Manager panel\nhttp://209.38.x.x", fontsize=7.5)
box(ax, 5.9, 1.0, 2.4, 2.7, "#3a1a3a", "Loki + Promtail",
    "log aggregation\nstructured JSON\npod log collection", fontsize=7.5)
box(ax, 8.5, 1.0, 2.7, 2.7, "#3a1a3a", "Alertmanager",
    "HighErrorRate\nHighLatency\nCrashLooping alerts", fontsize=7.5)

# ── DISCORD (right) ────────────────────────────────────────────────────────
group(ax, 12.1, 3.0, 2.8, 3.5, "#2a2040", "Notifications")
box(ax, 12.3, 3.4, 2.4, 2.7, "#352a50", "Discord",
    "CI status\nArgoCD syncs\nAlert webhooks", fontsize=8)

# ── TERRAFORM label ────────────────────────────────────────────────────────
ax.text(15.2, 5.5, "Terraform\nIaC", ha="center", va="center",
        color=C_PURPLE, fontsize=10, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#2a1a3a", edgecolor=C_PURPLE, lw=1.5))
ax.text(15.2, 4.7, "DOKS cluster\nHelm releases\nVPC · Node pool", ha="center", va="center",
        color=C_SUBTEXT, fontsize=7.5)

# ── ARROWS ─────────────────────────────────────────────────────────────────
# Developer → Pre-commit
arrow(ax, 1.6, 11.0, 1.6, 10.7)
# Pre-commit → GitHub repo (off-panel, show as git push)
arrow(ax, 2.7, 10.25, 3.6, 10.25, label="git push")
# GitHub CI internal
arrow(ax, 4.8, 11.2, 4.8, 10.8)  # lint→build
arrow(ax, 7.2, 11.2, 7.2, 10.8)  # test→manifest
arrow(ax, 5.0, 9.8, 5.3, 9.4)    # build→notify
arrow(ax, 7.0, 9.8, 6.8, 9.4)    # manifest→notify
# Build → Docker Hub
arrow(ax, 5.0, 10.3, 9.3, 10.5, label="push image")
# Manifest update → ArgoCD
arrow(ax, 6.0, 9.25, 2.0, 8.8, C_GREEN, label="manifest change")
# ArgoCD → App
arrow(ax, 3.3, 7.85, 3.9, 7.85, C_GREEN, label="sync")
# Docker Hub → App
arrow(ax, 9.3, 10.1, 5.1, 8.5, C_BLUE, label="pull image")
# App → Postgres
arrow(ax, 6.1, 7.85, 6.3, 7.85)
# Sealed secret → App
arrow(ax, 5.0, 6.0, 5.0, 7.2, C_YELLOW, label="inject secret")
# Prometheus → App (scrape)
arrow(ax, 2.0, 3.7, 4.0, 7.2, C_ORANGE, label="scrape /metrics")
# Loki → App (logs)
arrow(ax, 7.1, 3.7, 5.9, 7.2, C_ORANGE, label="collect logs")
# Prometheus → Grafana
arrow(ax, 3.1, 2.35, 3.3, 2.35)
# Loki → Grafana
arrow(ax, 5.9, 2.35, 5.7, 2.35)
# Prometheus → Alertmanager
arrow(ax, 3.1, 1.7, 8.5, 1.7)
# Alertmanager → Discord
arrow(ax, 11.2, 2.35, 12.3, 2.35, C_PURPLE, label="alerts")
# ArgoCD → Discord
arrow(ax, 1.4, 6.8, 12.3, 4.5, C_PURPLE, label="sync events")
# CI → Discord
arrow(ax, 6.0, 8.9, 12.3, 5.0, C_PURPLE, label="CI status")

# ── Legend ─────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color=C_ARROW, label="Data / deploy flow"),
    mpatches.Patch(color=C_GREEN, label="GitOps sync"),
    mpatches.Patch(color=C_ORANGE, label="Observability"),
    mpatches.Patch(color=C_YELLOW, label="Secrets"),
    mpatches.Patch(color=C_PURPLE, label="Notifications / IaC"),
]
ax.legend(handles=legend_items, loc="lower right", framealpha=0.3,
          facecolor="#1a1a2a", edgecolor=C_BORDER, labelcolor=C_TEXT, fontsize=8)

plt.tight_layout(pad=0.5)
plt.savefig("/home/to6eto/devops-task-manager/docs/architecture-diagram.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved: docs/architecture-diagram.png")
