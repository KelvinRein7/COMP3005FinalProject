from program import *
from helpers import *

def getFitnessGoals(memberID, cur):
    cur.execute("SELECT description FROM FitnessGoals WHERE memberID = %s", (memberID,))
    fitness_goals = cur.fetchall()
    return fitness_goals

def getRoutines(memberID, cur):
    cur.execute("SELECT description FROM Routines WHERE memberID = %s", (memberID,))
    routines = cur.fetchall()
    return routines

def getAchievements(memberID, cur):
    cur.execute("SELECT achieveDescription FROM Achievements WHERE memberID = %s", (memberID,))
    achievements = cur.fetchall()
    return achievements

def getBill(memberID, cur):
    cur.execute("SELECT amount, paymentDate FROM BillPayment WHERE memberID = %s", (memberID,))
    bill_info = cur.fetchall()
    return bill_info

def getMemberSessions(memberID, cur):
    cur.execute("""
        SELECT Session.time, Session.date, Session.status, Trainer.firstname, Trainer.lastname
        FROM Session
        INNER JOIN Trainer ON Session.trainerID = Trainer.trainerID
        WHERE Session.memberID = %s
    """, (memberID,))
    sessions = cur.fetchall()
    return sessions


def getMemberClasses(memberID, cur):
    cur.execute("SELECT time, date, status FROM FitnessClasses WHERE memberID = %s", (memberID,))
    classes = cur.fetchall()
    return classes

def getHealthMetrics(memberID, cur):
    cur.execute("SELECT gender, age, weight, height FROM Member WHERE memberID = %s", (memberID,))
    health_metrics = cur.fetchone()
    return health_metrics

def getMemberID(id, cursor):
    cursor.execute("SELECT memberID FROM Member WHERE loginID = %s", (id,))
    memberID = cursor.fetchone()[0]
    return memberID

def payBill(memberID, connection, cursor):
    try:
        # Check if the bill amount is already 0
        cursor.execute("SELECT amount FROM BillPayment WHERE memberID = %s", (memberID,))
        current_amount = cursor.fetchone()[0]
        if current_amount == 0:
            print("No bill to pay.")
        else:
            # Update the bill amount to 0 for the specified memberID
            cursor.execute("UPDATE BillPayment SET amount = 0.00 WHERE memberID = %s", (memberID,))
            connection.commit()
            print("Bill payment successful!")
    except Error as e:
        connection.rollback()
        print(f"Error during bill payment: {e}")



#register
def register(username, password, firstname, lastname, phone, address, email, gender, age, weight, height, connection, cursor):
    try:
        # Retrieve the most recent loginID
        cursor.execute("SELECT MAX(loginID) FROM UserLogin")
        max_loginID = cursor.fetchone()[0]
        
        # Increment the loginID
        new_loginID = max_loginID + 1
        
        # Insert user details into UserLogin table
        cursor.execute("INSERT INTO UserLogin (loginID, username, password) VALUES (%s, %s, %s) RETURNING loginID", (new_loginID, username, password))
        
        # Retrieve the most recent memberID
        cursor.execute("SELECT MAX(memberID) FROM Member")
        max_memberID = cursor.fetchone()[0]
        
        # Increment the memberID
        new_memberID = max_memberID + 1
        
        # Insert member details into Member table
        cursor.execute("INSERT INTO Member (memberID, loginID, firstname, lastname, phone, address, email, gender, age, weight, height) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (new_memberID, new_loginID, firstname, lastname, phone, address, email, gender, age, weight, height))
        
        # Outstanding bill as soon as user registered
        cursor.execute("SELECT MAX(billID) FROM BillPayment")
        max_billID = cursor.fetchone()[0]
        new_billID = max_billID + 1

        cursor.execute("INSERT INTO BillPayment (billID, memberID, amount, paymentDate) VALUES (%s, %s, %s, CURRENT_DATE)", (new_billID, new_memberID, 100.00))

        # Commit changes to the database
        connection.commit()
        
        print("Registration successful!")
        
    except Error as e:
        connection.rollback()
        print(f"Error during registration: {e}")

def createAchievement(memberID, description, cursor, connection):
    try:
        # Retrieve the most recent achievementID
        cursor.execute("SELECT MAX(achieveID) FROM Achievements")
        max_achievementID = cursor.fetchone()[0]

        # Increment the achievementID
        new_achievementID = max_achievementID + 1

        # Insert the new achievement into the database
        cursor.execute("INSERT INTO Achievements (achieveID, memberID, achieveDescription) VALUES (%s, %s, %s)", (new_achievementID, memberID, description))
        connection.commit()

        print("Achievement created successfully!")

    except Exception as e:
        connection.rollback()
        print(f"Error creating achievement: {e}")

def createFitnessGoals(memberID, description, cursor, connection):
    try:
        # Retrieve the most recent fitness goal
        cursor.execute("SELECT MAX(goalID) FROM FitnessGoals")
        max_fitnessgoalsID = cursor.fetchone()[0]

        # Increment the goalID
        new_fitnessgoalsID = max_fitnessgoalsID + 1

        # Insert the new goal into the database
        cursor.execute("INSERT INTO FitnessGoals (goalID, memberID, description) VALUES (%s, %s, %s)", (new_fitnessgoalsID, memberID, description))
        connection.commit()

        print("Fitness Goal created successfully!")

    except Exception as e:
        connection.rollback()
        print(f"Error creating fitness goals: {e}")

def createRoutine(memberID, description, cursor, connection):
    try:
        # Retrieve the most recent routineID
        cursor.execute("SELECT MAX(routineID) FROM Routines")
        max_routineID = cursor.fetchone()[0]

        # Increment the routineID
        new_routineID = max_routineID + 1

        # Insert the new routine into the database
        cursor.execute("INSERT INTO Routines (routineID, memberID, description) VALUES (%s, %s, %s)", (new_routineID, memberID, description))
        connection.commit()

        print("New Routine created successfully!")

    except Exception as e:
        connection.rollback()
        print(f"Error creating routine: {e}")

def createRoutine(memberID, description, cursor, connection):
    try:
        # Retrieve the most recent achievementID
        cursor.execute("SELECT MAX(routineID) FROM Routines")
        max_routineID = cursor.fetchone()[0]

        # Increment the achievementID
        new_routineID = max_routineID + 1

        # Insert the new achievement into the database
        cursor.execute("INSERT INTO Routines (routineID, memberID, description) VALUES (%s, %s, %s)", (new_routineID, memberID, description))
        connection.commit()

        print("Achievement created successfully!")

    except Exception as e:
        connection.rollback()
        print(f"Error creating achievement: {e}")

def bookSession(memberID, cursor, connection):
    try:
        # Retrieve the list of trainers and their availability
        cursor.execute("SELECT Trainer.trainerID, Trainer.firstname, Trainer.lastname, Availability.start_time, Availability.available_date FROM Trainer INNER JOIN Availability ON Trainer.trainerID = Availability.trainer_id")
        trainers_availability = cursor.fetchall()

        if not trainers_availability:
            print("No trainers available for booking.")
            return

        # Display the list of trainers and their availability to the user
        print("Trainers Availability:")
        for row in trainers_availability:
            trainer_id, firstname, lastname, start_time, available_date = row
            print(f"Trainer ID: {trainer_id}, Name: {firstname} {lastname}, Available Time: {start_time}, Date: {available_date}")

        # Prompt the user to input the trainer ID they want to book
        print()
        trainer_id_to_book = int(input("Enter the ID of the trainer you want to book: "))

        # Insert a new session associated with the memberID and the chosen trainerID

        cursor.execute("SELECT MAX(sessionID) FROM Session")
        max_sessionID = cursor.fetchone()[0]
        
        # Increment the loginID
        new_sessionID = max_sessionID + 1
        
        cursor.execute("INSERT INTO Session (sessionID, memberID, trainerID, time, date, status) VALUES (%s, %s, %s, %s, %s, %s)", (new_sessionID, memberID, trainer_id_to_book, start_time, available_date, 'Scheduled'))
        connection.commit()

        cursor.execute("INSERT INTO TrainerViewMember (trainerID, memberID) VALUES (%s, %s)", (trainer_id_to_book, memberID))
        connection.commit()

        print("Session booked successfully!\n")

    except Error as e:
        connection.rollback()
        print(f"Error during session booking: {e}")

def bookClasses(memberID, cursor, connection):
    try:
        # Retrieve the list of trainers and their availability
        cursor.execute("SELECT Trainer.trainerID, Trainer.firstname, Trainer.lastname, Availability.start_time, Availability.available_date FROM Trainer INNER JOIN Availability ON Trainer.trainerID = Availability.trainer_id")
        trainers_availability = cursor.fetchall()

        if not trainers_availability:
            print("No trainers available for booking.")
            return

        # Display the list of trainers and their availability to the user
        print("Trainers Availability:")
        for row in trainers_availability:
            trainer_id, firstname, lastname, start_time, available_date = row
            print(f"Trainer ID: {trainer_id}, Name: {firstname} {lastname}, Available Time: {start_time}, Date: {available_date}")

        # Prompt the user to input the trainer ID they want to book
        print()
        trainer_id_to_book = int(input("Enter the ID of the trainer you want to book: "))

        # Insert a new session associated with the memberID and the chosen trainerID

        cursor.execute("SELECT MAX(classID) FROM FitnessClasses")
        max_classID = cursor.fetchone()[0]
        
        # Increment the loginID
        new_classID = max_classID + 1
        
        cursor.execute("INSERT INTO FitnessClasses (classID, memberID, trainerID, time, date, status) VALUES (%s, %s, %s, %s, %s, %s)", (new_classID, memberID, trainer_id_to_book, start_time, available_date, 'Scheduled'))
        connection.commit()

        cursor.execute("INSERT INTO TrainerViewMember (trainerID, memberID) VALUES (%s, %s)", (trainer_id_to_book, memberID))
        connection.commit()

        print("Fitness Class booked successfully!\n")

    except Error as e:
        connection.rollback()
        print(f"Error during class booking: {e}")

#for member
def memberOptions(memberID, cur, conn):
    
    while True:

        print()
        print("1: View Fitness Goals")
        print("2: View Routines")
        print("3: View Achievements")
        print("4: View Health Metrics")
        print("5: View Fitness Sessions")
        print("6: View Fitness Classes")
        print("7: View Bill")
        print("---------------------------")
        print("8: Set Fitness Goals") 
        print("9: Set Routines")
        print("10: Set Achievements")
        print("11: Book Fitness Sessions")
        print("12: Book Fitness Classes")
        print("13: Pay Bill")
        print("0: Exit\n")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            #View Fitnessgoals
            id = getMemberID(memberID, cur)
            fitness_goals = getFitnessGoals(id, cur)
            if fitness_goals:
                print("Fitness Goals:")
                for goal in fitness_goals:
                    print(goal[0])
            else:
                print("You have not set fitness goals!\n")
        
        elif choice == "2":
            #View Routines
            id = getMemberID(memberID, cur)
            routines = getRoutines(id, cur)
            if routines:
                print("Routines:")
                for routine in routines:
                    print(routine[0])
            else:
                print("You have not set any routines!\n")

        elif choice == "3":
            #View Achievements
            id = getMemberID(memberID, cur)
            achievements = getAchievements(id, cur)
            if achievements:
                print("Achievements:")
                for achievement in achievements:
                    print(achievement[0])
            else:
                print("You have not achieved anything yet!\n")

        elif choice == "4":
            #View Healthmetrics
            id = getMemberID(memberID, cur)
            health_metrics = getHealthMetrics(id, cur)
            if health_metrics:
                gender, age, weight, height = health_metrics
                print("Your Health Metrics:")
                print("Gender:", gender)
                print("Age:", age)
                print("Weight:", weight, "kg")
                print("Height:", height, "cm")
                print()
            else:
                print("No health metrics found!\n")

        elif choice == "5":
            #View Sessions
            id = getMemberID(memberID, cur)
            sessions = getMemberSessions(id, cur)
            if sessions:
                print("Fitness Sessions:")
                for session in sessions:
                    print("Session Detail -> Date:", session[1], "Time:", session[0], "Status:", session[2])
            else:
                print("No fitness sessions found!\n")

        elif choice == "6":
            #View classes
            id = getMemberID(memberID, cur)
            classes = getMemberClasses(id, cur)
            if classes:
                print("Fitness Classes:")
                for class_info in classes:
                    print("Class Detail -> Date:", class_info[1], "Time:", class_info[0], "Status:", class_info[2])
                    print()
            else:
                print("No fitness classes found!\n")

        elif choice == "7":
            #View bill
            id = getMemberID(memberID, cur)
            bill_info = getBill(id, cur)
            if bill_info:
                print("Bill:")
                for info in bill_info:
                    print("Amount:", info[0], "Payment Date:", info[1])
                    print()
            else:
                print("No bill information found!\n")

        elif choice == "8":
            # Create Fitness Goals
            id = getMemberID(memberID, cur)
            fitnessgoals = getFitnessGoals(memberID, cur)
            if not fitnessgoals:
                description = input("Enter your fitness goals: ")
                createFitnessGoals(id, description, cur, conn)
            else:
                print("You can view your fitness goals!\n")

        elif choice == "9":
            # Create Fitness Goals
            id = getMemberID(memberID, cur)
            routine = getRoutines(memberID, cur)
            if not routine:
                description = input("Enter your new routine: ")
                createRoutine(id, description, cur, conn)
            else:
                print("You can view your routines!\n")
        
        elif choice == "10":
            # Create Achievement
            id = getMemberID(memberID, cur)
            achievements = getAchievements(memberID, cur)
            if not achievements:
                description = input("Enter your achievement description: ")
                createAchievement(id, description, cur, conn)
            else:
                print("You can view your achievements!\n")

        elif choice == "11":
            #Book Session
            id = getMemberID(memberID, cur)  # Assuming you have a function to get loginID from memberID
            if not getMemberSessions(memberID, cur):
                bookSession(id, cur, conn)  # Pass loginID instead of memberID
            else:
                print("You already have a session booked!\n")

        elif choice == "12":
            #Book Classes
            id = getMemberID(memberID, cur)  # Assuming you have a function to get loginID from memberID
            if not getMemberClasses(memberID, cur):
                bookClasses(id, cur, conn)  # Pass loginID instead of memberID
            else:
                print("You already have a class booked!\n")
        
        elif choice == "13":
            #pay bill
            id = getMemberID(memberID, cur)
            if not getBill(memberID, cur):
                payBill(id, conn, cur)
            else:
                print("You have no outstanding bill!")

        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")
