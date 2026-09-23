const appointmentsTable = document.getElementById("appointmentsTable");
const appointmentCount = document.getElementById("appointmentCount");
const refreshBtn = document.getElementById("refreshBtn");

function showMessage(message) {
    appointmentsTable.innerHTML = `
        <tr>
            <td colspan="5" class="loading">
                ${message}
            </td>
        </tr>
    `;
}


async function loadAppointments() {
    showMessage("Loading appointments...");

    try {
        const response = await fetch("/admin/appointments");

        if (response.status === 401) {
            showMessage("Admin login required.");
            return;
        }

        const result = await response.json();

        if (!result.success) {
            showMessage("Unable to load appointments.");
            return;
        }

        appointmentCount.textContent = result.appointments.length;

        if (result.appointments.length === 0) {
            showMessage("No appointments found.");
            return;
        }

        appointmentsTable.innerHTML = "";

        result.appointments.forEach((appointment) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${appointment.name}</td>
                <td>${appointment.phone}</td>
                <td>${appointment.department}</td>
                <td>${appointment.doctor}</td>
                <td>${appointment.date}</td>
            `;

            appointmentsTable.appendChild(row);
        });

    } catch (error) {
        console.error("Admin error:", error);
        showMessage("Unable to connect to the hospital server.");
    }
}

refreshBtn.addEventListener("click", loadAppointments);

loadAppointments();