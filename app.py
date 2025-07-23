from flask import Flask, request, jsonify, render_template
import pandas as pd
import random
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

FLIGHT_CSV = "airline_flights.csv"
BOOKING_CSV = "airline_bookings.csv"

def init_csv_files():
    """Ensures the CSV files exist with underscore_separated headers."""
    flight_cols = ["Flight_ID", "Departure_city", "Arriving_city", "Date", "Departure_time", "Arrival_time"]
    booking_cols = ["Booking_ID", "Flight_ID", "Name", "Age", "Gender", "Passport_NO", "Phone_NO"]

    if not os.path.exists(FLIGHT_CSV):
        pd.DataFrame(columns=flight_cols).to_csv(FLIGHT_CSV, index=False)

    if not os.path.exists(BOOKING_CSV):
        pd.DataFrame(columns=booking_cols).to_csv(BOOKING_CSV, index=False)

def clean_df_columns(df):
    """Helper function to replace spaces with underscores in column names."""
    df.columns = df.columns.str.replace(' ', '_')
    return df

# The @app.before_first_request decorator and setup() function have been removed.

@app.route("/")
def home():
    """Serves the main HTML page."""
    return render_template("index.html")

@app.route("/api/flights", methods=["GET"])
def get_flights():
    """Returns all flights from the CSV file with clean column names."""
    try:
        df = pd.read_csv(FLIGHT_CSV)
        df = clean_df_columns(df)
        return jsonify(df.to_dict(orient="records"))
    except FileNotFoundError:
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/flights", methods=["POST"])
def add_flight():
    """Adds a new flight to the CSV file."""
    try:
        data = request.json
        df = pd.DataFrame([data])
        
        if not os.path.exists(FLIGHT_CSV) or os.path.getsize(FLIGHT_CSV) == 0:
            df.to_csv(FLIGHT_CSV, header=True, index=False, mode='a')
        else:
            df.to_csv(FLIGHT_CSV, header=False, index=False, mode='a')
            
        return jsonify({"message": "Flight added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/bookings", methods=["POST"])
def book_flight():
    """Books a flight for a passenger."""
    try:
        data = request.json
        flights_df = pd.read_csv(FLIGHT_CSV)
        flights_df = clean_df_columns(flights_df)
        if data['Flight_ID'] not in flights_df['Flight_ID'].values:
            return jsonify({"error": "Invalid Flight ID"}), 404

        data["Booking_ID"] = random.randint(1000, 9999)
        df = pd.DataFrame([data])

        if not os.path.exists(BOOKING_CSV) or os.path.getsize(BOOKING_CSV) == 0:
            df.to_csv(BOOKING_CSV, header=True, index=False, mode='a')
        else:
            df.to_csv(BOOKING_CSV, header=False, index=False, mode='a')

        return jsonify({"message": "Booking successful", "booking_id": data["Booking_ID"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/bookings", methods=["GET"])
def view_bookings():
    """Returns all bookings from the CSV file with clean column names."""
    try:
        df = pd.read_csv(BOOKING_CSV)
        df = clean_df_columns(df)
        return jsonify(df.to_dict(orient="records"))
    except FileNotFoundError:
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/bookings/<booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    """Cancels a booking by its ID."""
    try:
        df = pd.read_csv(BOOKING_CSV)
        df = clean_df_columns(df)

        df['Booking_ID'] = df['Booking_ID'].astype(str)
        booking_id = str(booking_id)

        if booking_id not in df["Booking_ID"].values:
            return jsonify({"error": "Booking ID not found."}), 404

        df = df[df["Booking_ID"] != booking_id]
        df.to_csv(BOOKING_CSV, index=False)
        return jsonify({"message": "Booking cancelled."})
    except FileNotFoundError:
        return jsonify({"error": "No bookings found."}), 404
    except Exception as e:
        return jsonify({"error": f"Error cancelling booking: {e}"}), 500

if __name__ == "__main__":
    # FIX: Run the one-time setup function here, before starting the app.
    init_csv_files()
    app.run(port="3000", debug=True)