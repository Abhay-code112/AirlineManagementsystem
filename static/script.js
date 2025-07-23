document.addEventListener('DOMContentLoaded', () => {
    // --- State and Constants ---
    const API_FLIGHTS = '/api/flights';
    const API_BOOKINGS = '/api/bookings';

    // --- DOM Elements ---
    const flightsContainer = document.getElementById('flights-table-container');
    const bookingsContainer = document.getElementById('bookings-table-container');
    const addFlightModal = document.getElementById('add-flight-modal');
    const bookFlightModal = document.getElementById('book-flight-modal');
    const closeButtons = document.querySelectorAll('.close-btn');
    const addFlightForm = document.getElementById('add-flight-form');
    const bookFlightForm = document.getElementById('book-flight-form');
    const addFlightBtn = document.getElementById('add-flight-btn');

    // --- Toast Notifications ---
    const toast = document.getElementById('toast');
    function showToast(message, type = 'success') {
        toast.textContent = message;
        toast.style.backgroundColor = type === 'success' ? 'var(--success-color)' : 'var(--danger-color)';
        toast.className = 'show';
        setTimeout(() => { toast.className = toast.className.replace('show', ''); }, 3000);
    }

    // --- API Helper ---
    async function apiRequest(url, options = {}) {
        try {
            const response = await fetch(url, options);
            const responseData = await response.json(); // Always try to parse JSON
            if (!response.ok) {
                // Use the error message from the backend if available
                const errorMessage = responseData.error || `HTTP error! status: ${response.status}`;
                throw new Error(errorMessage);
            }
            return responseData;
        } catch (error) {
            console.error('API Request Failed:', error);
            showToast(error.message, 'error');
            return null;
        }
    }

    // --- Render Functions ---
    const createTable = (headers, data, actionButtons) => {
        if (!data || data.length === 0) {
            return '<p>No records found.</p>';
        }
        const table = document.createElement('table');
        const thead = table.createTHead();
        const tbody = table.createTBody();
        const headerRow = thead.insertRow();
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header.replace(/_/g, ' '); // Display with spaces
            headerRow.appendChild(th);
        });
        if (actionButtons) {
            const th = document.createElement('th');
            th.textContent = 'Actions';
            headerRow.appendChild(th);
        }

        data.forEach(item => {
            const row = tbody.insertRow();
            headers.forEach(header => {
                const cell = row.insertCell();
                // FIX: Access item directly with the underscore header. No replacement needed.
                cell.textContent = item[header];
            });
            if (actionButtons) {
                const cell = row.insertCell();
                actionButtons.forEach(buttonInfo => {
                    const button = document.createElement('button');
                    button.innerHTML = `<i class="fas ${buttonInfo.icon}"></i> ${buttonInfo.text}`;
                    button.className = buttonInfo.className;
                    button.dataset.id = item[buttonInfo.dataIdField];
                    cell.appendChild(button);
                });
            }
        });
        return table;
    };

    const renderFlights = (flights) => {
        const headers = ['Flight_ID', 'Departure_city', 'Arriving_city', 'Date', 'Departure_time', 'Arrival_time'];
        const actions = [{ text: 'Book Now', icon: 'fa-ticket-alt', className: 'btn btn-success', dataIdField: 'Flight_ID' }];
        flightsContainer.innerHTML = '';
        flightsContainer.appendChild(createTable(headers, flights, actions));
    };

    const renderBookings = (bookings) => {
        const headers = ['Booking_ID', 'Flight_ID', 'Name', 'Passport_NO', 'Phone_NO'];
        const actions = [{ text: 'Cancel', icon: 'fa-trash-alt', className: 'btn btn-danger', dataIdField: 'Booking_ID' }];
        bookingsContainer.innerHTML = '';
        bookingsContainer.appendChild(createTable(headers, bookings, actions));
    };

    // --- Load Initial Data ---
    async function loadAllData() {
        const flights = await apiRequest(API_FLIGHTS);
        if (flights) renderFlights(flights);

        const bookings = await apiRequest(API_BOOKINGS);
        if (bookings) renderBookings(bookings);
    }

    // --- Event Handlers ---
    addFlightForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const flightData = {
            'Flight_ID': document.getElementById('flight-id').value,
            'Departure_city': document.getElementById('departure-city').value,
            'Arriving_city': document.getElementById('arriving-city').value,
            'Date': new Date(document.getElementById('date').value).toLocaleDateString('en-GB'),
            'Departure_time': document.getElementById('departure-time').value,
            'Arrival_time': document.getElementById('arrival-time').value,
        };
        const result = await apiRequest(API_FLIGHTS, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(flightData)
        });
        if (result) {
            showToast('Flight added successfully!');
            addFlightForm.reset();
            addFlightModal.style.display = 'none';
            loadAllData();
        }
    });

    bookFlightForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const bookingData = {
            'Flight_ID': document.getElementById('book-flight-id-input').value,
            'Name': document.getElementById('name').value,
            'Age': document.getElementById('age').value,
            'Gender': document.getElementById('gender').value,
            'Passport_NO': document.getElementById('passport-no').value,
            'Phone_NO': document.getElementById('phone-no').value,
        };
        const result = await apiRequest(API_BOOKINGS, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookingData)
        });
        if (result) {
            showToast(`Booking successful! ID: ${result.booking_id}`);
            bookFlightForm.reset();
            bookFlightModal.style.display = 'none';
            loadAllData();
        }
    });

    // --- Modal Handling ---
    addFlightBtn.onclick = () => addFlightModal.style.display = 'block';
    closeButtons.forEach(btn => btn.onclick = () => {
        addFlightModal.style.display = 'none';
        bookFlightModal.style.display = 'none';
    });
    window.onclick = (event) => {
        if (event.target == addFlightModal || event.target == bookFlightModal) {
            addFlightModal.style.display = 'none';
            bookFlightModal.style.display = 'none';
        }
    };
    
    // --- Event Delegation for Dynamic Buttons ---
    document.body.addEventListener('click', async (e) => {
        const button = e.target.closest('button');
        if (!button) return;

        // Book Now button
        if (button.classList.contains('btn-success')) {
            const flightId = button.dataset.id;
            document.getElementById('book-flight-id-input').value = flightId;
            document.getElementById('booking-flight-details').textContent = `Booking for Flight: ${flightId}`;
            bookFlightModal.style.display = 'block';
        }
        // Cancel button
        if (button.classList.contains('btn-danger')) {
            const bookingId = button.dataset.id;
            if (confirm(`Are you sure you want to cancel booking ${bookingId}?`)) {
                const result = await apiRequest(`${API_BOOKINGS}/${bookingId}`, { method: 'DELETE' });
                if (result) {
                    showToast('Booking cancelled successfully!');
                    loadAllData();
                }
            }
        }
    });

    // --- Initial Load ---
    loadAllData();
});