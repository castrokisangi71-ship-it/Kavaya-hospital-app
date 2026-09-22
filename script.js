// =========================
// APPOINTMENT FORM
// =========================

const appointmentForm = document.querySelector(".appointment form");
const formMessage = document.getElementById("formMessage");


appointmentForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const department = document.getElementById("department").value;
    const doctor = document.getElementById("doctor").value;
    const date = document.getElementById("date").value;


    // Check required fields
    if (
        !name ||
        !email ||
        !phone ||
        !department ||
        !doctor ||
        !date
    ) {

        formMessage.textContent =
            "Please fill in all appointment details.";

        formMessage.className = "form-message error";

        return;
    }


    // Appointment data
    const appointment = {
        name: name,
        email: email,
        phone: phone,
        department: department,
        doctor: doctor,
        date: date
    };


    try {

const response = await fetch("http://127.0.0.1:5000/book-appointment", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(appointment)
        });


        const result = await response.json();


        // Successful booking
        if (result.success) {

            appointmentForm.reset();

            formMessage.textContent =
                "Appointment booked successfully! Thank you, " +
                name +
                ".";

            formMessage.className =
                "form-message success";

        }


        // Server returned an error
        else {

            formMessage.textContent =
                "Something went wrong. Please try again.";

            formMessage.className =
                "form-message error";

        }

    }


    // Server connection error
    catch (error) {

        console.error("Appointment error:", error);

        formMessage.textContent =
            "Unable to connect to the hospital server.";

        formMessage.className =
            "form-message error";
    }

});
// =========================
// APPOINTMENT DATE
// =========================

const appointmentDate = document.getElementById("date");

if (appointmentDate) {

    const today = new Date();

    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");

    const todayString = `${year}-${month}-${day}`;

    appointmentDate.min = todayString;
}