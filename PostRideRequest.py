import sqlite3
import sys
from ValidateInputs import*

def PostRequest(user):

    print("========")
    print("Post a ride request:")

    while True:
        dateInput = input("Please enter the date of your ride (YYYY-MM-DD)> ")
        if Vali_Date(dateInput) is False:
            print("Format incorrect, please enter a date in the YYYY-MM-DD format only (for example: 2018-05-26)")
        else:
            break

    while True:
        pickupCode = ValidateLocation(input("Pickup location>"))
        if pickupCode is not False:
            break

    while True:
        dropoffCode = ValidateLocation(input("Dropoff Location>"))
        if dropoffCode is not False:
            break

    while True:
        Payment = GetInteger(input("Amount you are willing to pay ($) >"))
        if Payment is not False:
            break

    conn = sqlite3.connect("./"+sys.argv[1])
    c = conn.cursor()

    c.execute("select COALESCE(max(rid)+1,0)from requests")
    currentRID = c.fetchone()

    c.execute("INSERT INTO requests VALUES(?,?,?,?,?,?)", (currentRID[0], user[0], dateInput, pickupCode, dropoffCode, Payment))
    conn.commit()

    print("========")
    print("Request successfully posted!")

    return True
