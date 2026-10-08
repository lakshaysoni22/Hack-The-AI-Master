#!/usr/bin/env bash
# Resets the TechCorp Access Control lab to its original state.
# Only touches files inside this project's own database/ directory.
set -e

cd "$(dirname "$0")"

echo "== TechCorp Access Control Lab — Reset =="

if [ -d "venv" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
fi

echo "[*] Removing existing lab database (if any)..."
rm -f database/techcorp.db

echo "[*] Recreating users and initial data..."
python3 -c "from app import init_db; init_db()"

echo "[*] Lab reset complete. Restart the app with ./start.sh"
