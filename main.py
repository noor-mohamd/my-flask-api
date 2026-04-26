from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            job_title TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "<h1>Backend API Status: Online</h1><p>The Flask server is running successfully.</p>"

@app.route('/add', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    job = data.get('job_title')
    
    if not username or not job:
        return jsonify({"error": "Missing data"}), 400
        
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, job_title) VALUES (?, ?)", (username, job))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    users_list = []
    for row in rows:
        users_list.append({"id": row[0], "username": row[1], "job_title": row[2]})
        
    return jsonify(users_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)