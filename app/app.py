import sqlite3
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "votes.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE,
            vote TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

OPTIONS = [
    {"id": "cats", "label": "Cats", "icon": "🐱", "color": "#ec4899"},
    {"id": "dogs", "label": "Dogs", "icon": "🐶", "color": "#3b82f6"},
]

@app.route("/")
def index():
    return render_template("index.html", options=OPTIONS)

@app.route("/api/results", methods=["GET"])
def get_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT vote, COUNT(*) FROM votes GROUP BY vote")
    rows = cursor.fetchall()
    conn.close()

    counts = {opt["id"]: 0 for opt in OPTIONS}
    total = 0
    for vote, count in rows:
        if vote in counts:
            counts[vote] = count
            total += count

    results = []
    for opt in OPTIONS:
        count = counts[opt["id"]]
        percentage = round((count / total * 100), 1) if total > 0 else 0
        results.append({
            "id": opt["id"],
            "label": opt["label"],
            "icon": opt["icon"],
            "color": opt["color"],
            "count": count,
            "percentage": percentage
        })

    return jsonify({"total": total, "results": results})

@app.route("/api/vote", methods=["POST"])
def submit_vote():
    data = request.get_json() or {}
    vote = data.get("vote")
    voter_id = request.remote_addr or "anonymous"

    valid_ids = [opt["id"] for opt in OPTIONS]
    if vote not in valid_ids:
        return jsonify({"error": "Invalid vote option"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO votes (voter_id, vote) VALUES (?, ?) ON CONFLICT(voter_id) DO UPDATE SET vote=excluded.vote",
            (voter_id, vote)
        )
        conn.commit()
        success = True
        message = "Vote recorded successfully!"
    except Exception as e:
        success = False
        message = str(e)
    finally:
        conn.close()

    if success:
        return jsonify({"success": True, "message": message, "voted": vote})
    return jsonify({"error": message}), 500

@app.route("/api/reset", methods=["POST"])
def reset_votes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM votes")
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Votes reset!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
