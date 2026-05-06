from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="../templates"
)

DB_PATH = "/tmp/pinoysmm.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT NOT NULL,
                service TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT DEFAULT 'Processing',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        default_stats = {
            "followers": 1000000,
            "likes": 5000000,
            "posts": 120,
            "reach": 2500000
        }

        for key, value in default_stats.items():
            conn.execute(
                "INSERT OR IGNORE INTO stats (key, value) VALUES (?, ?)",
                (key, value)
            )

        conn.commit()


def get_stats():
    with get_db() as conn:
        rows = conn.execute("SELECT key, value FROM stats").fetchall()
        return {row["key"]: row["value"] for row in rows}


init_db()


@app.route("/")
def home():
    return render_template("index.html", stats=get_stats())


@app.route("/api/stats", methods=["GET"])
def api_stats():
    return jsonify({
        "status": "success",
        "stats": get_stats()
    })


@app.route("/update/<key>/<int:amount>", methods=["POST"])
@app.route("/api/update/<key>/<int:amount>", methods=["POST"])
def update_stat(key, amount):
    stats = get_stats()

    if key not in stats:
        return jsonify({
            "status": "error",
            "message": "Key not found"
        }), 404

    with get_db() as conn:
        conn.execute(
            "UPDATE stats SET value = value + ? WHERE key = ?",
            (amount, key)
        )
        conn.commit()

    new_stats = get_stats()

    return jsonify({
        "status": "success",
        "key": key,
        "new_value": new_stats[key],
        "stats": new_stats
    })


@app.route("/api/order", methods=["POST"])
def create_order():
    try:
        data = request.get_json() or {}

        link = data.get("link", "").strip()
        service = data.get("service", "").strip()
        quantity_raw = data.get("quantity", 0)

        try:
            qty = int(quantity_raw)
        except ValueError:
            qty = 0

        if not link:
            return jsonify({
                "status": "error",
                "message": "Please enter a target link."
            }), 400

        if not service:
            return jsonify({
                "status": "error",
                "message": "Please select a service."
            }), 400

        if qty <= 0:
            return jsonify({
                "status": "error",
                "message": "Quantity must be greater than 0."
            }), 400

        with get_db() as conn:
            conn.execute(
                "INSERT INTO orders (link, service, quantity) VALUES (?, ?, ?)",
                (link, service, qty)
            )
            conn.commit()

        # Demo effect: update stats after placing an order
        if "Follower" in service:
            stat_key = "followers"
        elif "Like" in service:
            stat_key = "likes"
        elif "Share" in service:
            stat_key = "reach"
        elif "Comment" in service:
            stat_key = "reach"
        else:
            stat_key = "reach"

        with get_db() as conn:
            conn.execute(
                "UPDATE stats SET value = value + ? WHERE key = ?",
                (qty, stat_key)
            )
            conn.commit()

        return jsonify({
            "status": "success",
            "message": f"🚀 Demo order created: {qty:,} {service} for {link}",
            "stats": get_stats()
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
