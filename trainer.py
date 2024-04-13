from program import *
from helpers import *

#for trainer
def getAssignedClasses(loginID, cur):
    cur.execute("SELECT classID, memberID, time, date, status FROM FitnessClasses WHERE trainerID = (SELECT trainerID FROM Trainer WHERE loginID = %s)", (loginID,))
    return cur.fetchall()

def getAssignedSessions(loginID, cur):
    cur.execute("SELECT sessionID, memberID, time, date, status FROM Session WHERE trainerID = (SELECT trainerID FROM Trainer WHERE loginID = %s)", (loginID,))
    return cur.fetchall()

def getTrainerSchedule(loginID, cur):
    cur.execute("SELECT scheduleID, time FROM TrainerSchedule WHERE trainerID = (SELECT trainerID FROM Trainer WHERE loginID = %s)", (loginID,))
    return cur.fetchall()

def getTrainerMembers(loginID, cur):
    cur.execute("SELECT Member.memberID, Member.firstname, Member.lastname, Member.phone FROM TrainerViewMember JOIN Member ON TrainerViewMember.memberID = Member.memberID WHERE TrainerViewMember.trainerID = (SELECT trainerID FROM Trainer WHERE loginID = %s)", (loginID,))
    return cur.fetchall()

def getMemberName(memberID, cursor):
    try:
        # Execute the SQL query to retrieve member name
        cursor.execute("SELECT firstname, lastname FROM Member WHERE memberID = %s", (memberID,))
        member = cursor.fetchone()

        # Check if member exists
        if member:
            firstname, lastname = member
            return f"{firstname} {lastname}"
        else:
            return "Member not found"

    except Error as e:
        print(f"Error fetching member name: {e}")
        return None

def getMemberGoals(memberID, cursor):
    try:
        cursor.execute("SELECT description FROM FitnessGoals WHERE memberID = %s", (memberID,))
        goals = cursor.fetchall()
        return goals
    except Error as e:
        print(f"Error fetching member's goals: {e}")
        return None

def getMemberDetails(memberID, cursor):
    try:
        cursor.execute("SELECT gender, age, weight, height FROM Member WHERE memberID = %s", (memberID,))
        member_details = cursor.fetchone()
        return member_details  # Returns a tuple of (height, weight, age)
    except Exception as e:
        print(f"Error retrieving member details: {e}")
        return None
    
def getTrainerFirstName(trainerID, cursor):
    try:
        cursor.execute("SELECT firstname FROM Trainer WHERE trainerID = %s", (trainerID,))
        trainer_firstname = cursor.fetchone()[0]
        return trainer_firstname
    except Error as e:
        print(f"Error retrieving trainer's first name: {e}")
        return None
    
def setAvailability(trainerID, start_time, available_date, cur, conn):
    try:
        # Check if the availability already exists for the same time and date
        cur.execute("SELECT availability_id FROM Availability WHERE start_time = %s AND available_date = %s AND trainer_id = %s", (start_time, available_date, trainerID))
        existing_availability = cur.fetchone()
        
        if existing_availability:
            print("Availability for the same time and date already exists.")
            return
        
        cur.execute("SELECT MAX(availability_id) FROM Availability")
        max_availID = cur.fetchone()[0]
        
        # Increment the loginID
        new_availID = max_availID + 1
        
        # If availability does not exist, insert the new availability
        cur.execute("INSERT INTO Availability (availability_id, start_time, available_date, trainer_id) VALUES (%s, %s, %s, %s)", (new_availID, start_time, available_date, trainerID))
        conn.commit()
        
        print("Availability set successfully!")
        print()
        
    except Error as e:
        conn.rollback()
        print(f"Error setting availability: {e}")

def getTrainerID(id, cursor):
    cursor.execute("SELECT trainerID FROM Trainer WHERE loginID = %s", (id,))
    trainerID = cursor.fetchone()[0]
    return trainerID


def trainerOptions(trainerID, cur, con):

    while True:

        print("1: View Trainer Schedule")
        print("2: View Assigned Sessions")
        print("3: View Assigned Classes")
        print("4: View Members")
        print("5: Set Availability")
        print("0: Exit\n")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            # View Trainer Schedule
            trainer_schedule = getTrainerSchedule(trainerID, cur)
            if trainer_schedule:
                print("Your Schedule:")
                for schedule in trainer_schedule:
                    print("Schedule ID:", schedule[0])
                    print("Time:", schedule[1])
                    print()
            else:
                print("No schedule found!\n")

        elif choice == "2":
            # View Assigned Sessions
            assigned_sessions = getAssignedSessions(trainerID, cur)
            if assigned_sessions:
                print("Assigned Sessions:")
                for session in assigned_sessions:
                    print("Session ID:", session[0])
                    print("Member:", getMemberName(session[1], cur))
                    print("Time:", session[2])
                    print("Date:", session[3])
                    print("Status:", session[4])
                    print()
            else:
                print("No assigned sessions found!\n")

        elif choice == "3":
            # View Assigned Classes
            assigned_classes = getAssignedClasses(trainerID, cur)
            if assigned_classes:
                print("Assigned Classes:")
                for class_info in assigned_classes:
                    print("Class ID:", class_info[0])
                    print("Member ID:", class_info[1])
                    print("Name:", getMemberName(class_info[1], cur))
                    print("Time:", class_info[2])
                    print("Date:", class_info[3])
                    print("Status:", class_info[4])
                    print()
            else:
                print("No assigned classes found!\n")

        elif choice == "4":
            # View Members
            trainer_members = getTrainerMembers(trainerID, cur)
            if trainer_members:
                name = getTrainerFirstName(getTrainerID(trainerID, cur), cur)
                print("Hi " + name + ", here are your trainees:")
                print()
                for member in trainer_members:
                    member_details = getMemberDetails(member[0], cur)
                    gender, age, weight, height = member_details
                    print("Member ID:", member[0])
                    print("Name:", member[1] + " " + member[2])
                    print("Gender:", gender)
                    print("Age:", age)
                    print("Weight", weight, "kg")
                    print("Height", height, "cm")
                    goals = getMemberGoals(member[0], cur)
                    formatted_goals = ", ".join(goal[0] for goal in goals)
                    print("Goals:", formatted_goals)
                    print()
            else:
                print("No members assigned to this trainer!\n")
        
        elif choice == "5":
            # Set Availability
            id = getTrainerID(trainerID, cur)
            start_time = input("Enter start time (HH:MM): ")
            available_date = input("Enter available date (YYYY-MM-DD): ")
            print()
            setAvailability(id, start_time, available_date, cur, con)

        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")