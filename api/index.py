from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder="../templates")

DB_PATH = os.getenv("DATABASE_URL", "/tmp/smm_database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pinoy_pool (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                tier TEXT,
                activity_score INTEGER
            )
        """)
        conn.commit()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/order", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        link = data.get("link")
        service = data.get("service")
        qty = int(data.get("quantity"))

        with get_db() as conn:
            conn.execute(
                "INSERT INTO orders (link, service, quantity) VALUES (?, ?, ?)",
                (link, service, qty)
            )
            conn.commit()

        return jsonify({
            "status": "success",
            "message": f"🚀 {qty} {service} deployed to {link}"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
