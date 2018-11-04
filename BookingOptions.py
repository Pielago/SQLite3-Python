from ValidateInputs import*

def BookMember(user):
    conn = sqlite3.connect('./Database.db')
    c = conn.cursor()
    print("========")
    print("Rides offered by you:") # replace with name or nah?
    c.execute("select * from bookings where email=?", (user[0],))
    bookingResults = c.fetchall()
    print(bookingResults)

    print("========")
    print("Offering rides:(Optional, leave blank if not applicable)")
