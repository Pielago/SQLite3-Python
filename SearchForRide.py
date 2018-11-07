from ValidateInputs import*
import sys

def RideSearch(user):
    print("========")
    print("Search for rides:(mandatory fields)")

    rides = getRide()
    msg = input("Please enter your message>")
    conn = sqlite3.connect("./"+sys.argv[1])
    c = conn.cursor()

    c.execute("INSERT INTO inbox VALUES(?,datetime('now'),?,?,?,?)", (rides[7], user[0], msg, rides[0], 0))

    conn.commit()
    return


