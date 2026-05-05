python:api/index.py
from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Path to database - optimized for Vercel's ephemeral file system
DB_PATH = os.getenv("DATABASE_URL", "smm_database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB: Ensures the "Non-Drop" tables exist
def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT NOT NULL,
                service TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT DEFAULT 'Processing',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # The "Non-Drop" User Pool
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pinoy_pool (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                tier TEXT, -- 'Real', 'High-Quality', 'Premium'
                activity_score INTEGER -- Higher = Less likely to drop
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        link = data.get('link')
        service = data.get('service')
        qty = int(data.get('quantity'))
        
        with get_db() as conn:
            conn.execute('INSERT INTO orders (link, service, quantity) VALUES (?, ?, ?)', 
                         (link, service, qty))
            conn.commit()
            
        return jsonify({"status": "success", "message": f"🚀 {qty} {service} deployed to {link}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Vercel Handler: The bridge between Flask and Serverless
def handler(request, context):
    return app(request)

# Run this once to seed the DB if running locally
if __name__ == "__main__":
    init_db()
    app.run()
