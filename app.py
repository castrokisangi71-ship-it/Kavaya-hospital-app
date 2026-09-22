from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

APPOINTMENTS_FILE = "appointments.json"


def save_appointment(appointment):
    appointments = []

    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "r") as file:
            try:
                appointments = json.load(file)
            except json.JSONDecodeError:
                appointments = []

    appointments.append(appointment)

    with open(APPOINTMENTS_FILE, "w") as file:
        json.dump(appointments, file, indent=4)


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

    save_appointment(appointment)

    return jsonify({
        "success": True,
        "message": "Appointment booked successfully."
    })


if __name__ == "__main__":
    app.run(debug=True)