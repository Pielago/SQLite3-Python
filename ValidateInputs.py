import sys
import sqlite3

#
# This file is mostly to just hold misc functions that are gonna be called
#
from datetime import datetime

#Validate the date
def Vali_Date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def getLocation():
    while True:
        ExactSucc = input("Enter your location and select from the list>")
        succ = "%" + ExactSucc + "%"
        conn = sqlite3.connect("./"+sys.argv[1])
        c = conn.cursor()
        c.execute("select * from locations where city like ? COLLATE NOCASE or address like ? COLLATE NOCASE or prov like ? COLLATE NOCASE or lcode like ? COLLATE NOCASE ", (succ, succ, succ, ExactSucc))

        LocationResults = c.fetchall()

        if LocationResults:
            break
        print("Sorry, your keyword didn't return any results, please try a different keyword>")
    a = 0
    b = 5
    while True:
        for n in range(len(LocationResults[a:b])):
            print(n + a, "  :  ", LocationResults[n + a])

        x = input("Enter the number of your intended location or enter X to scroll up or Z to scroll down>")
        if x.isdigit() and (a <= int(x) <= a+len(LocationResults[a:b])):
            return LocationResults[int(x)][0]

        elif x.upper() == 'X' and a >= 0:
            a -= 5
            b -= 5
        elif x.upper() == 'Z' and a <= len(LocationResults):
            a += 5
            b += 5
        else:
            print("Invalid input, try again>")

def getBookings(user):
    while True:
        conn = sqlite3.connect("./"+sys.argv[1])
        c = conn.cursor()
        c.execute("SELECT * FROM rides WHERE driver = ? COLLATE NOCASE", (user[0],))
        bookingResults = c.fetchall()

        if not bookingResults:
            print("Sorry, you don't have any rides offered. Please enter rides in the main menu.")
            return False

        a = 0
        b = 5
        while True:
            for n in range(len(bookingResults[a:b])):
                print(n + a, "  :  The ride is from",bookingResults[n + a][5], "to",bookingResults[n + a][6], "with", bookingResults[n + a][3], "seats, and a carryon of", bookingResults[n + a][4],"with a cost of", bookingResults[n + a][1], "on", bookingResults[n + a][2])

            x = input("Enter the number of the ride you would like to book a member on"
                      " or enter X to scroll up or Z to scroll down>")
            if x.isdigit() and (a <= int(x) <= a+len(bookingResults[a:b])):
                if int(bookingResults[int(x)][3]) <= 0:
                    confirm = input("This ride is currently fully booked. Would you still like to book it? (Y/N)>")
                    if confirm.upper() == 'Y':
                        return bookingResults[int(x)]
                    elif confirm.upper() == 'N':
                        break
                else:
                    return bookingResults[int(x)]
                    break
            elif x.upper() == 'X' and a >= 0:
                a -= 5
                b -= 5
            elif x.upper() == 'Z' and a <= len(bookingResults):
                a += 5
                b += 5
            else:
                print("Invalid input, try again>")

def getRequests():
    while True:
        ExactSucc = input("Enter your location and select from the list>")
        succ = "%" + ExactSucc + "%"
        conn = sqlite3.connect("./"+sys.argv[1])
        c = conn.cursor()
        c.execute("select* from requests, locations where pickup = lcode and (city like ? COLLATE NOCASE or lcode like ? COLLATE NOCASE )", (succ, ExactSucc))

        RequestResults = c.fetchall()

        if RequestResults:
            break
        print("Sorry, your keyword didn't return any results, please try a different keyword>")

    a = 0
    b = 5
    while True:
        for n in range(len(RequestResults[a:b])):
            print(n + a, "  :  ", "Driven by ",RequestResults[n + a][1], "on", RequestResults[n + a][2], "from", RequestResults[n + a][3], "to", RequestResults[n + a][4], "for the price of $", RequestResults[n + a][5])

        x = input("Enter the number of your intended request or enter X to scroll up or Z to scroll down>")
        if x.isdigit() and (a <= int(x) <= a+len(RequestResults[a:b])):
            return RequestResults[int(x)][1]
            break
        elif x.upper() == 'X' and a >= 0:
            a -= 5
            b -= 5
        elif x.upper() == 'Z' and a <= len(RequestResults):
            a += 5
            b += 5
        else:
            print("Invalid input, try again>")

def ValidateLocation(locationCode):
    conn = sqlite3.connect("./"+sys.argv[1])
    c = conn.cursor()
    c.execute("select lcode from locations")

    locationsTuples = c.fetchall()
    locationsList = [i[0] for i in locationsTuples]

    if locationCode in locationsList:
        return locationCode
    else:
        print("Location code does not exists, please try again>")
        return False
    return True

def GetInteger(testInteger):
    if testInteger.isdigit():
        return testInteger
    else:
        print("Sorry, please enter an integer value>")
        return False

def getRide():
    while True:

        succ = input("Please enter 1-3 location keywords separated by spaces> ").split()
        succ = ['%' + x + '%' for x in succ]
        conn = sqlite3.connect("./"+sys.argv[1])
        c = conn.cursor()
        if len(succ) == 1:
            c.execute("SELECT DISTINCT r.rno, price, rdate, seats, lugDesc, src, dst, driver, cno FROM rides r, "
                      "enroute e, locations l WHERE (l.city like ?) AND ((l.lcode = e.lcode AND r.rno = e.rno) "
                      "OR (l.lcode = r.src) OR (l.lcode = r.dst))", succ)
        elif len(succ) == 2:
            c.execute("SELECT DISTINCT r.rno, price, rdate, seats, lugDesc, src, dst, driver, cno FROM rides r, "
                      "enroute e, locations l WHERE (l.city like ? OR l.city like ?) AND ((l.lcode = e.lcode AND r.rno "
                      "= e.rno) OR (l.lcode = r.src) OR (l.lcode = r.dst))", (succ[0], succ[1]))
        elif len(succ) == 3:
            c.execute("SELECT DISTINCT r.rno, price, rdate, seats, lugDesc, src, dst, driver, cno FROM rides r, "
                      "enroute e, locations l WHERE (l.city like ? OR l.city like ? OR l.city like ?) AND "
                      "((l.lcode = e.lcode AND r.rno = e.rno) OR (l.lcode = r.src) OR (l.lcode = "
                      "r.dst))", (succ[0], succ[1], succ[2]))
        else:
            print("Please enter 1-3 keywords separated by spaces>")

        RideResults = c.fetchall()

        if RideResults:
            break
        print("Sorry, your keyword didn't return any results, please try a different keyword>")

    a = 0
    b = 5
    while True:
        for n in range(len(RideResults[a:b])):
            print(n + a, "  :  The ride is from",RideResults[n + a][5], "to",RideResults[n + a][6], "with", RideResults[n + a][3], "seats, and a carryon of", RideResults[n + a][4],"with a cost of", RideResults[n + a][1], "on", RideResults[n + a][2], "and the driver email is", RideResults[n + a][7])

        x = input("Enter X to scroll up and Z to scroll down. If there is a ride you would like to book then please "
                  "enter the number of the intended ride to message the member>")
        if x.isdigit() and (a <= int(x) <= a + len(RideResults[a:b])):
            return RideResults[int(x)]
            break
        elif x.upper() == 'X' and a >= 0:
            a -= 5
            b -= 5
        elif x.upper() == 'Z' and a <= len(RideResults):
            a += 5
            b += 5
        else:
            print("Invalid input, try again>")

def verifyCar(carNumber, user):
    conn = sqlite3.connect("./"+sys.argv[1])
    c = conn.cursor()
    c.execute("select * from cars where cno = ? and owner = ? COLLATE NOCASE", (carNumber, user[0]))
    car = c.fetchall()
    if not car:
        return False
    else:
        return True

def getEmail():
    while True:
        Email = input("Please enter passenger member email>")
        conn = sqlite3.connect("./"+sys.argv[1])
        c = conn.cursor()
        c.execute("select email from members where email = ? COLLATE NOCASE", (Email,))
        emailExists = c.fetchone()
        if emailExists:
            break
        else:
            print("sorry, the email you entered does not exist in the system, please try again")
    return Email