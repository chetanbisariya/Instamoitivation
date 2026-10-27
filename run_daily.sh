#!/usr/bin/env bash
# ==============================================================
# Daily Instagram Reel Agent Launcher Script
# ==============================================================
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Ensure virtual environment python is used
PYTHON_BIN="$DIR/.venv/bin/python"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Virtual environment not found at $PYTHON_BIN. Please run python3 -m venv .venv first."
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Triggering daily reel automation..."
"$PYTHON_BIN" -m agent.runner --now "$@" >> "$DIR/output/agent_run.log" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Completed."
