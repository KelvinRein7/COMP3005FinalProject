from program import *
from helpers import *

#for admin
def getEquipments(cur):
    cur.execute("SELECT * FROM Equipments")
    equipments = cur.fetchall()
    return equipments

def getBookingsAndRooms(cur):
    cur.execute("SELECT b.bookingID, r.roomID, r.roomName, b.time FROM Bookings b INNER JOIN Rooms r ON b.roomID = r.roomID")
    bookings_and_rooms = cur.fetchall()
    return bookings_and_rooms

def getBillPayments(cur):
    #Bill payments + User's names
    cur.execute("""
        SELECT bp.billID, bp.memberID, bp.amount, bp.paymentDate, m.firstname, m.lastname 
        FROM BillPayment bp
        INNER JOIN Member m ON bp.memberID = m.memberID
    """)
    bill_payments = cur.fetchall()
    return bill_payments

def getFitnessClasses(cur):
    # Fetch all fitness classes along with member and trainer details
    cur.execute("""
        SELECT fc.classID, fc.memberID, fc.trainerID, fc.time, fc.date, fc.status, 
               m.firstname AS member_firstname, m.lastname AS member_lastname, 
               t.firstname AS trainer_firstname, t.lastname AS trainer_lastname
        FROM FitnessClasses fc
        INNER JOIN Member m ON fc.memberID = m.memberID
        INNER JOIN Trainer t ON fc.trainerID = t.trainerID
    """)
    fitness_classes = cur.fetchall()
    return fitness_classes


def getSessions(cur):
    # Fetch all fitness sessions along with member and trainer details
    cur.execute("""
        SELECT s.sessionID, s.memberID, s.trainerID, s.time, s.date, s.status, 
               m.firstname AS member_firstname, m.lastname AS member_lastname, 
               t.firstname AS trainer_firstname, t.lastname AS trainer_lastname
        FROM Session s
        INNER JOIN Member m ON s.memberID = m.memberID
        INNER JOIN Trainer t ON s.trainerID = t.trainerID
    """)
    sessions = cur.fetchall()
    return sessions


def adminOptions(adminID, cur):

    while True:

        print("1: View Equipments")
        print("2: View Bookings and Rooms")
        print("3: View Bill Payment")
        print("4: View Fitness Classes")
        print("5: View Fitness Sessions")
        print("0: Exit\n")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            equipments = getEquipments(cur)
            if equipments:
                print("Equipments:")
                for equipment in equipments:
                    print("Equipment ID:", equipment[0])
                    print("Name:", equipment[1])
                    print("Maintenance Date:", equipment[2])
                    print()
            else:
                print("No equipments found!\n")

        elif choice == "2":
            #View Bookings and Rooms
            bookings_and_rooms = getBookingsAndRooms(cur)
            if bookings_and_rooms:
                print("Bookings and Rooms:")
                print()
                for booking_room in bookings_and_rooms:
                    print("Booking ID:", booking_room[0])
                    print("Room ID:", booking_room[1])
                    print("Room Name:", booking_room[2])
                    print("Time:", booking_room[3])
                    print()
            else:
                print("No bookings and rooms found!\n")

        elif choice == "3":
            # View Bill Payment
            bill_payments = getBillPayments(cur)
            if bill_payments:
                print("Bill Payments:")
                print()
                for bill_payment in bill_payments:
                    print("Bill ID:", bill_payment[0])
                    print("Member ID:", bill_payment[1])
                    print("Member Name:", bill_payment[4], bill_payment[5])  # First name and last name
                    print("Amount:", bill_payment[2])
                    print("Payment Date:", bill_payment[3])
                    print()
            else:
                print("No bill payments found!\n")

        elif choice == "4":
            # View Fitness Classes
            classes = getFitnessClasses(cur)
            if classes:
                print("Fitness Classes:")
                print()
                for class_info in classes:
                    print("Class ID:", class_info[0])
                    print("Member Name:", class_info[6], class_info[7])  # First name and last name of member
                    print("Trainer Name:", class_info[8], class_info[9])  # First name and last name of trainer
                    print("Time:", class_info[3])
                    print("Date:", class_info[4])
                    print("Status:", class_info[5])
                    print()
            else:
                print("No fitness classes found!\n")

        elif choice == "5":
            # View Fitness Sessions
            sessions = getSessions(cur)
            if sessions:
                print("Fitness Sessions:")
                print()
                for session in sessions:
                    print("Session ID:", session[0])
                    print("Member Name:", session[6], session[7])  # First name and last name of member
                    print("Trainer Name:", session[8], session[9])  # First name and last name of trainer
                    print("Time:", session[3])
                    print("Date:", session[4])
                    print("Status:", session[5])
                    print()
            else:
                print("No fitness sessions found!\n")

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")