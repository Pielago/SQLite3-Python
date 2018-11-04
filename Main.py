# imports
import sqlite3
from memberOptions import *

# Login Screen
def login_menu():
    print ("\n")
    # We gonna leave this line out for now, don't want keywords for people to find on Github lul
    print("Welcome to J. Miller's Rideshare Database System")
    print("========")
    print("A - Existing Users: Login")
    print("B - New Users: Create Account")
    print("C - Exit")
    print("========")
    print("Type A B or C and hit enter to select an option")
    # Handles user menu choice
    while True:
        userInput = input("Function> ")
        if userInput.upper() in ('A','B', 'C'):
            return userInput.upper()
        else:
            print ("Input value not valid, please retry your option.")
            continue

#Prompt for username / password
def existing_user(conn):
    print ("\n")
    print ("Welcome returning user")
    print ("Please login with your account")
    print ("========")

    enteredEmail = input("Email> ")
    enteredPassword = input("Password> ")
    c = conn.cursor()
    c.execute("SELECT	*	FROM	members	WHERE	email=:try_email and	pwd=:try_password", {"try_email":enteredEmail,	"try_password":	enteredPassword})
    return c.fetchone()

def login_create(conn):
    c = conn.cursor()
    unique = True

    print ("\n")
    print ("Welcome new user")
    print ("Please follow these steps to sign up for an account")
    print ("========")

    while unique is True:
        duplicate = False
        enteredEmail = input("Enter your email address> ")
        for row in c.execute("SELECT	email	FROM	members"):
            if enteredEmail == row[0]:
                print("This email has been claimed by another user, please try a different email")
                duplicate = True
        if duplicate is False:
            unique = False

    enteredName = input("Enter your full name> ")
    enteredPhone = input("Enter your phone number> ")
    enteredPassword = input("Choose a password> ")
    c.execute("INSERT INTO members VALUES(?,?,?,?)", (enteredEmail,	enteredPhone, enteredName, enteredPassword ))
    conn.commit()
    print ("========")
    print ("Your account has been successfully set up! You can now login from the main screen.")
    conn.close()

def showInbox(conn, user):
    print("Here are your unread messages:")
    c = conn.cursor()
    c.execute("SELECT	*   FROM	inbox	WHERE	email=? and seen=0", (user[0],))
    inbox = c.fetchall()
    for i in range(len(inbox)):
        print("At ", inbox[i][1], ", ", inbox[i][2], " said to you: ", inbox[i][3])
        c.execute("UPDATE inbox SET seen=1")
        conn.commit()

    if not inbox:
        print("    (Inbox is empty, no unread messages)    ")

def main():
    # Create Inital Database Connection
    conn = sqlite3.connect('./Database.db')


    # Allow the user to select their inital task
    while True:
        userInput = login_menu()
        if userInput == 'A':
            user = existing_user(conn)
            if user is None:
                print("========")
                print("User not found, please retry")
                print("========")
            else:
                print("========")
                print("Welcome Lord", user[1])
                print("========")
                showInbox(conn, user)
                memberOptions(user)

        elif userInput == 'B':
            login_create(conn)
            conn = sqlite3.connect('./Database.db')
        elif userInput == 'C':
            print("========")
            print("Goodbye JoJo")
            break
        # Get associated information, connect to module.

if __name__ == "__main__":
    main()
