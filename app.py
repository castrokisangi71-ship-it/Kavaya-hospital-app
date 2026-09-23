from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import secrets
import psycopg

app = Flask(__name__)
CORS(app)
ADMIN_KEY = os.environ.get("ADMIN_KEY")
app.secret_key = SECRET_KEY
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")
    return psycopg.connect(DATABASE_URL)


def create_table():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id BIGSERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    department TEXT NOT NULL,
                    doctor TEXT NOT NULL,
                    appointment_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()

@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json() or {}
    key = data.get("key")

    if not ADMIN_KEY:
        return jsonify({
            "success": False,
            "message": "Admin key is not configured."
        }), 500

    if not secrets.compare_digest(key or "", ADMIN_KEY):
        return jsonify({
            "success": False,
            "message": "Invalid admin key."
        }), 401

    session["admin_authenticated"] = True

    return jsonify({
        "success": True,
        "message": "Admin login successful."
    })
@app.route("/admin/appointments", methods=["GET"])
def get_appointments():
    if not session.get("admin_authenticated"):
        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 401

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name,
                    email,
                    phone,
                    department,
                    doctor,
                    appointment_date
                FROM appointments
                ORDER BY appointment_date ASC, id DESC
            """)

            rows = cursor.fetchall()

    appointments = []

    for row in rows:
        appointments.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "department": row[4],
            "doctor": row[5],
            "date": str(row[6])
        })

    return jsonify({
        "success": True,
        "appointments": appointments
    })
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


@app.route("/book-appointment", methods=["POST"])
def book_appointment():

    data = request.get_json()

    appointment = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "department": data.get("department"),
        "doctor": data.get("doctor"),
        "date": data.get("date")
    }

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO appointments
                (name, email, phone, department, doctor, appointment_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                appointment["name"],
                appointment["email"],
                appointment["phone"],
                appointment["department"],
                appointment["doctor"],
                appointment["date"]
            ))
        conn.commit()

    return jsonify({
        "success": True,
        "message": "Appointment booked successfully."
    })


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
else:
    create_table()