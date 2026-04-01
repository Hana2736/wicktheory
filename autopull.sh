#!/bin/bash
# Auto-poll GitHub and rebuild container on changes
# Runs on the remote server (oraclecloud)

set -euo pipefail

REPO_DIR="/home/hana/candlestore_Gui"
BRANCH="main"
POLL_INTERVAL="${1:-60}"  # seconds, default 60

cd "$REPO_DIR"

echo "[autopull] Watching $REPO_DIR (branch: $BRANCH) every ${POLL_INTERVAL}s"

while true; do
    # Fetch latest from remote
    git fetch origin "$BRANCH" 2>/dev/null

    LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "none")
    REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "none")

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "[autopull] $(date '+%F %T') Change detected ($LOCAL -> $REMOTE), pulling and rebuilding..."
        git reset --hard "origin/$BRANCH"
        docker compose down
        docker compose up -d --build
        echo "[autopull] $(date '+%F %T') Rebuild complete."
    fi

    sleep "$POLL_INTERVAL"
done
