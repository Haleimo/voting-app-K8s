#!/usr/bin/env bash
set -e

echo "🚀 Starting Lightweight Voting App..."

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

if python3 -c "import flask" 2>/dev/null; then
    echo "✓ Flask detected."
else
    echo "Installing requirements..."
    pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt
fi

export PORT=${PORT:-5000}
echo "Running server at http://localhost:${PORT} ..."
python3 app/app.py
