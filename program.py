import psycopg2
from psycopg2 import Error
from datetime import date
from helpers import *
from members import *
from admin import *
from trainer import *

# Database connection info
hostname = "localhost"
dbname = "Health and Fitness"
username = "postgres"
dbpassword = "1234"
portnumber = "5432"

# Connect to PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(
            user=username,
            password=dbpassword,
            host=hostname,
            database=dbname,
            port=portnumber
        )
        return connection
    except Error as e:
        print(f"Error while connecting to the database: {e}")
        return None

# User login function
def login(username, password):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Check if username and password match
        cursor.execute("SELECT * FROM UserLogin WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            if(isMember(username, cursor)):
                memberOptions(user[0], cursor, connection)
            elif(isTrainer(username, cursor)):
                trainerOptions(user[0], cursor, connection)
            elif(isAdmin(username, cursor)):
                adminOptions(user[0], cursor)
            else:
                print("You must be new!!")
            
        # else:
        #     print("Invalid username or password")

        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error during login: {e}")

# Main function
def main():

    connection = connect()
    cursor = connection.cursor()

    while True:
        print("\nWelcome to Health and Fitness Management System")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            print()
            login(username, password)

        elif choice == "2":
            #Registration process
            print("\nRegistration:")
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            firstname = input("Enter your first name: ")
            lastname = input("Enter your last name: ")
            phone = input("Enter your phone number: ")
            address = input("Enter your address: ")
            email = input("Enter your email: ")
            gender = input("Enter your gender (M/F): ")
            age = int(input("Enter your age: "))
            weight = float(input("Enter your weight (kg): "))
            height = float(input("Enter your height (cm): "))
            register(username, password, firstname, lastname, phone, address, email, gender, age, weight, height, connection, cursor)

        elif choice == "3":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
