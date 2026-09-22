from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import psycopg

app = Flask(__name__)
CORS(app)


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