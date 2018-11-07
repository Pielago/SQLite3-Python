from ValidateInputs import*


def BookingOptions(user):
    conn = sqlite3.connect("./"+sys.argv[1])
    c = conn.cursor()
    print("========")
    print("Bookings for rides offered by you:")
    while True:
        c.execute("select b.bno, b.email, b.rno, b.cost, b.seats, b.pickup, b.dropoff from rides r, bookings b where "
                  "r.rno = b.rno  and driver = ? COLLATE NOCASE", (user[0],))
        bookingResults = c.fetchall()
        for n in range(len(bookingResults[0:len(bookingResults)])):
            print(n, "  :  The booking is from",bookingResults[n][5], "to",bookingResults[n][6], "with", bookingResults[n][4], "seats, a cost of", bookingResults[n][3], "and the member email is", bookingResults[n][1])

        print("========")
        while True:
            x = input("Please enter in A to cancel a booking, B to add a booking or C to quit.")
            if x.upper() == 'A':
                if not bookingResults:
                    print("You have no bookings, add bookings in previous screen")
                    break

                y = int(input("Please enter the number of the booking you would like to cancel."))
                c.execute("DELETE FROM bookings WHERE bno = ?", (bookingResults[y][0],))
                msg = input("Please enter a message informing the member that you have cancelled the booking.")
                c.execute("INSERT INTO inbox VALUES(?,datetime('now'),?,?,?,?)", (bookingResults[y][1], user[0], msg,
                                                                                  bookingResults[y][2], 0))
                c.execute("UPDATE rides SET seats = seats + ? WHERE rno = ?", (bookingResults[y][4],
                                                                               bookingResults[y][2]))
                conn.commit()
                print("========")
                print("Booking successfully cancelled:")
                print("========")
                break
            elif x.upper() == 'B':
                booking = getBookings(user)
                if booking is False:
                    return
                ridenum = booking[0]
                while True:
                    numSeats = input("Please enter the number of seats that are being booked or enter X to exit out.")
                    if numSeats == 'X' or numSeats == 'x':
                        return
                    elif int(numSeats) > int(booking[3]):
                        choice = input("This will overbook the ride. Are you sure you want "
                                       "to book this many seats? (Y/N)")
                        if choice.upper() == 'Y':
                            break
                        elif choice.upper() == 'N':
                            continue
                        else:
                            continue
                    else:
                        break
                memberEmail = getEmail()
                seatCost = input("Please enter the cost per seat in the booking.")
                while True:
                    pickup = ValidateLocation(input("Please enter a valid pickup location code."))
                    if pickup is not False:
                        break
                while True:
                    dropoff = ValidateLocation(input("Please enter a valid dropoff location code."))
                    if dropoff is not False:
                        break
                c.execute("select COALESCE(max(bno)+1,0)from bookings")
                currentBNO = c.fetchone()
                c.execute("INSERT INTO bookings VALUES(?,?,?,?,?,?,?)", (currentBNO[0], memberEmail, ridenum,
                                                                         seatCost, numSeats, pickup, dropoff))
                c.execute("UPDATE rides SET seats = seats - ? WHERE rno = ?", (numSeats, booking[0]))
                msg = input("Please enter your message to inform the member that you have booked them.")
                # is message custom or no?
                c.execute("INSERT INTO inbox VALUES(?,datetime('now'),?,?,?,?)", (memberEmail, user[0], msg,
                                                                                  ridenum, 0))
                conn.commit()
                print("========")
                print("Booking successfully added:")
                print("========")
                break
            elif x.upper() == 'C':
                return
            else:
                print("Invalid input.")
