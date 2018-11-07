# import the 5 program functions
from PostRideRequest import*
from RideRequestOptions import*
from SearchForRide import*
from BookingOptions import*
from OfferRide import*

def memberOptions(user):
    # Handles user menu choice
    while True:

        print("========")
        print("Main menu: What would you like to do?")
        print("========")
        print("A - Offer a ride")
        print("B - Search for a ride")
        print("C - Book a member or cancel booking")
        print("D - Post a request")
        print("E - Search or delete ride requests")
        print("Z - Logout")
        print("========")
        print("Type A B C D E or Z and hit enter to select option.")

        userInput = input("Function> ")
        if userInput.upper() in ('A', 'B', 'C', 'D', 'E', 'Z'):
            if userInput.upper() == 'A':
                OfferRide(user)
                print("========")
                print("Ride successfully created")
            elif userInput.upper() == 'B':
                RideSearch(user)
                print("========")
                print("Message sent to driver")
            elif userInput.upper() == 'C':
                BookingOptions(user)
            elif userInput.upper() == 'D':
                PostRequest(user)
            elif userInput.upper() == 'E':
                RequestOptions(user)
            elif userInput.upper() == 'Z':
                print("========")
                print("You are now logged out.")
                break
        else:
            print("Input value not valid, please retry your option.")
            continue
    return