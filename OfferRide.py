import sqlite3
from ValidateInputs import*

def OfferRide(user):
    print("========")
    print("Offering rides:(Mandatory Fields)")
    while True:
        dateInput = input("Please enter the date of your ride (YYYY-MM-DD)> ")
        if Vali_Date(dateInput) is False:
            print("Enter date properly you fuck")
        else:
            break
    seatNumber = input("Please enter the number of seat you are offering> ")
    seatPrice = input("Please enter your asking price for each seat ($)> ")
    luggage = input("Please enter a quick luggage description>")
    locationSrc = getLocation() #Returns LCODE

    locationDes = getLocation() #Returns LCODE

    print("========")
    print("Offering rides:(Optional, leave blank if not applicable)")

    carNumber = input("Please enter your car number> ")
    if not carNumber:
        #then no number was given
        carNumber = None


    print("Select enroute location")
    enrouteNumber = input("Please select the number of enroute locations you wish to enter (0 is ok)> ")
    enrouteLocations = [None] * int(enrouteNumber)


    conn = sqlite3.connect('./Database.db')
    c = conn.cursor()
    c.execute("select COALESCE(max(rno)+1,0)from rides")
    currentRNO = c.fetchone()

    c.execute("INSERT INTO rides VALUES(?,?,?,?,?,?,?,?,?)", (currentRNO[0], seatPrice, dateInput, seatNumber, luggage, locationSrc, locationDes, user[0], carNumber ))

    for n in range(len(enrouteLocations)):
        enrouteLocations[n] = getLocation()
        c.execute("INSERT INTO enroute VALUES(?,?)", (currentRNO[0], enrouteLocations[n]))

    conn.commit()

    conn.close()

    return True
