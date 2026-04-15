# ---- Stage 1: Build React frontend ----
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ---- Stage 2: Node.js backend runtime ----
FROM node:20-alpine

LABEL maintainer="devops-task-manager"

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY backend/package*.json ./
RUN npm ci --omit=dev

COPY backend/ .
COPY --from=frontend-build /app/backend/public ./public

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["node", "index.js"]
