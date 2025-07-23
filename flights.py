import pandas as pd
from utils import validate_date, validate_time, display_table

FLIGHT_CSV = "airline_flights.csv"

def add_flight():
    """Adds a new flight to the CSV file."""
    flight_id = input("Enter Flight ID: ").strip()
    departure_city = input("Enter Departure City: ").strip()
    arriving_city = input("Enter Arriving City: ").strip()

    while True:
        date = input("Enter Date (DD/MM/YYYY): ").strip()
        if validate_date(date):
            break
        print("Invalid date format!")

    while True:
        departure_time = input("Enter Departure Time (HH:MM): ").strip()
        if validate_time(departure_time):
            break
        print("Invalid time format!")

    while True:
        arrival_time = input("Enter Arrival Time (HH:MM): ").strip()
        if validate_time(arrival_time):
            break
        print("Invalid time format!")

    flight_data = {
        "Flight ID": [flight_id],
        "Departure city": [departure_city],
        "Arriving city": [arriving_city],
        "Date": [date],
        "Departure time": [departure_time],
        "Arrival time": [arrival_time]
    }

    df = pd.DataFrame(flight_data)
    with open(FLIGHT_CSV, 'a') as file:
        df.to_csv(file, header=file.tell() == 0, index=False)
    print("✅ Flight added successfully!")

def view_flights():
    """Displays all flights from the CSV file."""
    try:
        df = pd.read_csv(FLIGHT_CSV)
        display_table(df)
    except FileNotFoundError:
        print("❌ No flight data available yet.")

def remove_flight():
    """Removes a flight from the CSV file by its ID."""
    try:
        df = pd.read_csv(FLIGHT_CSV)
        display_table(df)
        flight_id = input("Enter Flight ID to remove: ").strip()
        if flight_id in df["Flight ID"].astype(str).values:
            df = df[df["Flight ID"].astype(str) != flight_id]
            df.to_csv(FLIGHT_CSV, index=False)
            print("✅ Flight removed successfully.")
        else:
            print("❌ Flight ID not found.")
    except FileNotFoundError:
        print("❌ No flight data found.")