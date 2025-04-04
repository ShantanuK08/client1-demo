from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Setup DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "TeamManager.db")

# Ensure table exists
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                coach TEXT,
                city TEXT
            )
        ''')
        conn.commit()

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        coach = data.get('coach')
        city = data.get('city')

        if not name:
            return jsonify({"error": "Team name is required"}), 400

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO teams (name, coach, city) VALUES (?, ?, ?)", (name, coach, city))
            conn.commit()
        return jsonify({"message": "Team added successfully"}), 201

    else:  # GET
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teams")
            teams = cursor.fetchall()
            return jsonify(teams), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
