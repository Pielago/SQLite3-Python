import sys
import sqlite3
from ValidateInputs import *
def RequestOptions(user):

    while True:
        print("========")
        print("To delete a request, enter 1")
        print("To search for requests to fulfill, press 2")

        nextStep = input("Choose>")
        if nextStep == '1':
            DeleteRequest(user)
            return
        elif nextStep == '2':
            SearchRequests(user)
            return
        else:
            print("Entry Invalid, please try again.")

def DeleteRequest(user):
    while True:
        print("========")
        print("To delete a request, enter the number beside the request. Or press X to cancel.")
        print("Here are all of your ride requests:")

        conn = sqlite3.connect("./"+sys.argv[1])
        c = conn.cursor()
        c.execute("select rdate, pickup, dropoff, amount, rid from requests where email = ? COLLATE NOCASE", (user[0], ))

        requestsList = c.fetchall()

        RIDList = [None] * len(requestsList)

        for n in range(len(requestsList)):
            print(n, "  :     On" , requestsList[n][0], "from",requestsList[n][1], "to", requestsList[n][2], "for the price of $",requestsList[n][3] )
            RIDList[n] = requestsList[n][4]

        if not RIDList:
            print("You have no currently active requests. Press X to quit")
        DeleteOption = input("Delete>")
        if DeleteOption.upper() == "X":
            return
        elif DeleteOption.isdigit() and 0 <= int(DeleteOption) <= len(requestsList):
            DeleteOption = int(DeleteOption)
            print(DeleteOption)
            c.execute(" delete from requests where rid = ?", (RIDList[DeleteOption], ))
            conn.commit()
        else:
            print("Invalid Entry, please try again")

def SearchRequests(user):
    print("========")
    print("Send a message to the driver of your chosen request.")
    print("To search for a request, search for the pickup location.")
    ChosenRequestDriver = getRequests()

    print("Enter message to send to the driver:")
    DriverMessage = input("Message>")

    conn = sqlite3.connect("./"+sys.argv[1])
    c = conn.cursor()
    c.execute("INSERT INTO inbox VALUES(?,datetime('now'),?,?, null, 0)", (ChosenRequestDriver, user[0], DriverMessage,))
    conn.commit()

    return