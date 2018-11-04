
import sqlite3

#
#This file to mostly just hold misc functions that're gonna be called a whole bunch
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


    return True

def getLocation():
    while True:

        succ = input("Enter your starting location and select from the list")
        succ = "%" + succ + "%"
        conn = sqlite3.connect('./Database.db')
        c = conn.cursor()
        c.execute("select * from locations where city like ? or address like ? or prov like ? or lcode like ?", (succ, succ, succ, succ))

        LocationResults = c.fetchall()

        if LocationResults:
            break
        print("Sorry, your keyword didn't return any results, please try a different keyword")
    a = 0
    b = 5
    while True:
        for n in range(len(LocationResults[a:b])):
            print(n + a, "  :  ", LocationResults[n + a])

        x = input("Enter the number of your intended location or enter X to scroll up or Z to scroll down")
        if x.isdigit() and (a <= int(x) <= a+4):
            return LocationResults[int(x)][0]
            break
        elif x.upper() == 'X' and a >= 0:
            a -= 5
            b -= 5
        elif x.upper() == 'Z':
            a += 5
            b += 5
        else:
            print("Invalid input, try again")
    return 1


def getRide():
    while True:

        succ = input("Please enter 1-3 location keywords separated by spaces> ").split()
        succ = ['%' + x + '%' for x in succ]
        conn = sqlite3.connect('./Database.db')
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
            print("Please enter 1-3 keywords separated by space.")

        RideResults = c.fetchall()

        if RideResults:
            break
        print("Sorry, your keyword didn't return any results, please try a different keyword")

    a = 0
    b = 5
    while True:
        for n in range(len(RideResults[a:b])):
            print(n + a, "  :  ", RideResults[n + a])

        x = input("Enter X to scroll up and Z to scroll down. If there is a ride you would like to book then please "
                  "enter the number of the intended ride to message the member.")
        if x.isdigit() and (a <= int(x) <= a + 4):
            return RideResults[int(x)]
            break
        elif x.upper() == 'X' and a >= 0:
            a -= 5
            b -= 5
        elif x.upper() == 'Z':
            a += 5
            b += 5
        else:
            print("Invalid input, try again")
    return 1


# def sendMessage(user, rides, msg):
#     conn = sqlite3.connect('./Database.db')
#     c = conn.cursor()
#
#     c.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", (rides[7], datetime('now'), user[0], msg, rides[0], 0))
