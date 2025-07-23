from flights import add_flight, view_flights, remove_flight
from bookings import book_flight, view_bookings, cancel_booking

def menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\n✈✈🛫 AIRLINE MANAGEMENT SYSTEM 🛬✈✈")
        print("By Abhay Kumar Kashyap")
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Remove Flight")
        print("4. Book Flight")
        print("5. View Bookings")
        print("6. Cancel Booking")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()
        actions = {
            "1": add_flight,
            "2": view_flights,
            "3": remove_flight,
            "4": book_flight,
            "5": view_bookings,
            "6": cancel_booking,
            "7": lambda: print("🛑 Exiting... Thank you!")
        }
        action = actions.get(choice)
        if action:
            if choice == "7":
                action()
                break
            action()
        else:
            print("❌ Invalid input, try again.")

if __name__ == "__main__":
    menu()