#Code is created by Abhay kumar kashyap
import pandas as pd
import random
def Addflight():
    Flight_ID = input("Enter the Flight ID: ")
    Departure_city = input("Enter the Departure city: ")
    Arriving_city = input("Enter the Arriving city: ")
    Date = input("Enter the Date (DD/MM/YYYY): ")

    departure_time = input("Enter departure time (HH:MM): ") 
    arrival_time = input("Enter arrival time (HH:MM): ")

    flight_data = {"Flight ID": [Flight_ID],"Departure city": [Departure_city],"Arriving city": [Arriving_city],"Date": [Date],"Departure time": [departure_time],"Arrival time": [arrival_time]
    }
    Data = pd.DataFrame(flight_data)
    with open("Airlinedata.csv",'a') as file:
        Data.to_csv(file,header=file.tell()==0,index=False)
    print("Flight added successfully!")

def ViewFlights():
    Data=pd.read_csv("Airlinedata.csv")
    print(Data)
def Removeflight():
     print("Available flights:")
     ViewFlights()
     Data=pd.read_csv("Airlinedata.csv")
     Flight_ID=int(input("Enter flight ID to remove the flight: "))
     print("Entered flight_ID",Flight_ID)
     if Flight_ID in Data["Flight ID"].values:
         Data=Data[Data["Flight ID"]!=Flight_ID]
         Data.to_csv("Airlinedata.csv",index=False)
         print("Flight removed successfuly")
     else:
         print("Flight already doesnot exists")   
def BookFlights():
    print("AVAILABLE FLIGHTS")
    ViewFlights()

    Data=pd.read_csv("Airlinedata.csv")
    print("Available Flight IDs:", Data['Flight ID'].values)
    Flight_ID=int(input("Enter the Flight_ID of the Flight: "))
    print("Entered Flight ID:", Flight_ID)
   

    if int(Flight_ID) in Data['Flight ID'].values:
        Booking_ID=random.randrange(100,200)
        print("Your booking ID: ",Booking_ID)
        Name=input("Enter the passenger's Name: ")
        Age=input("Enter passenger's age: ")
        Gender=input("Enter the gender of the passenger: ")
        Passport_NO=input("Enter passenger's passport number: ")
        Phone_NO=input("Enter the passenger's Phone number:")
        Booking_Data={"Booking_ID":[Booking_ID],"Name":[Name],"Age":[Age],"Gender":[Gender],"Passport_NO":[Passport_NO],"Phone_NO":Phone_NO}
        Bookings=pd.DataFrame(Booking_Data)
        with open("Airlinedata2.csv",'a') as file2:
            Bookings.to_csv(file2,header=file2.tell()==0,index=False)
        print("Flight Booked successfully")
    else:
        print("invalid")
    
   
    
def Viewbookings():
    Bookings=pd.read_csv("Airlinedata2.csv")

    print(Bookings[0:])
def cancelbookings():
    Viewbookings()
    Bookings=pd.read_csv("Airlinedata2.csv")
    print("Available Booking IDs:", Bookings['Booking_ID'].values)
    Booking_ID=int(input("Enter the Booking ID of the Flight to be canceled"))
    print("Entered Flight ID:", Booking_ID)
    if int(Booking_ID) in Bookings["Booking_ID"].values:
       Bookings = Bookings[Bookings['Booking_ID'] != Booking_ID]
       Bookings.to_csv("Airlinedata2.csv", index=False)
       print("Booking cancled successfully")
    else:
        print("INvalid booking id")

while True:
    print('''✈✈🛫🛬\tAIRLINE MANAGEMENT SYSTEM\t🛬🛫✈✈
             By Abhay Kumar Kashyap''')
    try:
        choice = int(input("1-Add_Flight\n2-View_Flights\n3-Remove_flight\n4-Book_Flights\n5-View_Bookings\n6-Cancel_Bookings\n7-exit\n"))
    except ValueError:
        print("Invalid input! Please enter a number.")
        continue    
    if choice == 8:
        print("Enter Valid Input!\n")
    match choice:
        case 1:
            Addflight()    
        case 2:
            ViewFlights()  
        case 3:  
            Removeflight()
        case 4:
            BookFlights()
        case 5:
            Viewbookings()
        case 6:
            cancelbookings()
        case 7:
            print("THANK YOU")
            exit(1)