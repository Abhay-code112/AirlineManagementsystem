import pandas as pd
import random
from utils import display_table, validate_phone

BOOKING_CSV = "airline_bookings.csv"
FLIGHT_CSV = "airline_flights.csv"

def book_flight():
    """Books a flight for a passenger."""
    try:
        df = pd.read_csv(FLIGHT_CSV)
        display_table(df)
    except FileNotFoundError:
        print("❌ No flights available.")
        return

    flight_id = input("Enter Flight ID to book: ").strip()
    if flight_id not in df["Flight ID"].astype(str).values:
        print("❌ Invalid Flight ID.")
        return

    booking_id = random.randint(1000, 9999)
    name = input("Enter Name: ").strip()
    age = input("Enter Age: ").strip()
    gender = input("Enter Gender: ").strip()
    passport_no = input("Enter Passport Number: ").strip()

    while True:
        phone_no = input("Enter Phone Number (10 digits): ").strip()
        if validate_phone(phone_no):
            break
        print("❌ Invalid phone number.")

    booking_data = {
        "Booking_ID": [booking_id],
        "Flight_ID": [flight_id],
        "Name": [name],
        "Age": [age],
        "Gender": [gender],
        "Passport_NO": [passport_no],
        "Phone_NO": [phone_no]
    }

    df = pd.DataFrame(booking_data)
    with open(BOOKING_CSV, 'a') as file:
        df.to_csv(file, header=file.tell() == 0, index=False)
    print(f"✅ Booking successful. Your Booking ID is {booking_id}")

def view_bookings():
    """Displays all bookings from the CSV file."""
    try:
        df = pd.read_csv(BOOKING_CSV)
        display_table(df)
    except FileNotFoundError:
        print("❌ No bookings available.")

def cancel_booking():
    """Cancels a booking by its ID."""
    try:
        df = pd.read_csv(BOOKING_CSV)
        display_table(df)
        booking_id = input("Enter Booking ID to cancel: ").strip()
        if booking_id in df["Booking_ID"].astype(str).values:
            df = df[df["Booking_ID"].astype(str) != booking_id]
            df.to_csv(BOOKING_CSV, index=False)
            print("✅ Booking cancelled.")
        else:
            print("❌ Booking ID not found.")
    except FileNotFoundError:
        print("❌ No bookings to cancel.")