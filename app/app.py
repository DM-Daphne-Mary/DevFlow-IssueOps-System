from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "complaintsdb"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "admin123")
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            complaint TEXT,
            status VARCHAR(20) DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("ALTER TABLE complaints ADD COLUMN IF NOT EXISTS category VARCHAR(100) DEFAULT 'General'")
    cur.execute("ALTER TABLE complaints ADD COLUMN IF NOT EXISTS priority VARCHAR(50) DEFAULT 'Medium'")
    conn.commit()
    cur.close()
    conn.close()

db_initialized = False
def ensure_db():
    global db_initialized
    if not db_initialized:
        try:
            init_db()
            db_initialized = True
        except Exception as e:
            print(f"Database not ready yet: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/complaints/open', methods=['GET'])
def get_open_complaints():
    ensure_db()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, complaint, status, created_at, category, priority FROM complaints WHERE status = 'Open' ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    complaints = [
        {"id": r[0], "name": r[1], "email": r[2],
         "complaint": r[3], "status": r[4], "created_at": str(r[5]), "category": r[6], "priority": r[7]}
        for r in rows
    ]
    return jsonify(complaints)

@app.route('/complaints', methods=['GET'])
def get_complaints():
    ensure_db()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, complaint, status, created_at, category, priority FROM complaints ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    complaints = [
        {"id": r[0], "name": r[1], "email": r[2],
         "complaint": r[3], "status": r[4], "created_at": str(r[5]), "category": r[6], "priority": r[7]}
        for r in rows
    ]
    return jsonify(complaints)

@app.route('/complaints', methods=['POST'])
def add_complaint():
    ensure_db()
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    category = data.get('category', 'General')
    priority = data.get('priority', 'Medium')
    cur.execute(
        "INSERT INTO complaints (name, email, complaint, category, priority) VALUES (%s, %s, %s, %s, %s)",
        (data['name'], data['email'], data['complaint'], category, priority)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Complaint submitted successfully!"}), 201

if __name__ == '__main__':
    ensure_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
