-- Inserting data into the User table
INSERT INTO UserLogin (loginID, username, password) 
VALUES 
    (1, 'user1', 'password1'),
	(2, 'user2', 'password2'),
	(3, 'user3', 'password3'),
    (4, 'user4', 'password4'),
	(5, 'user5', 'password5'),
	(6, 'trainer', 'trainer'),
    (7, 'user7', 'password7'),
	(8, 'admin', 'admin'),
	(9, 'user9', 'password9');

-- Inserting data into the Member table
INSERT INTO Member (memberID, loginID, firstname, lastname, phone, address, email, gender, age, weight, height) 
VALUES 
    (1, 1, 'John', 'Doe', '1234567890', '123 Main St', 'john@example.com', 'M', 30, 180.00, 70.00),
    (2, 2, 'Alice', 'Smith', '9876543210', '456 Elm St', 'alice@example.com', 'F', 25, 150.00, 65.00),
    (3, 3, 'Bob', 'Johnson', '5551234567', '789 Oak St', 'bob@example.com', 'M', 35, 160.00, 75.00);

-- Inserting data into the Trainer table
INSERT INTO Trainer (trainerID, loginID, firstname, lastname, phone) 
VALUES 
    (1, 4, 'Amad', 'Diallo', '1112223333'),
    (2, 5, 'Diogo', 'Dalot', '4445556666'),
    (3, 6, 'Bruno', 'Fernandes', '7778889999');

-- Inserting data into the TrainerMemberAccess table
INSERT INTO TrainerViewMember (trainerID, memberID) 
VALUES 
    (1, 1),
    (2, 2),
    (3, 3);

-- Inserting data into the Achievements table
INSERT INTO Achievements (achieveID, memberID, achieveDescription) 
VALUES 
    (1, 1, 'Ran a marathon'),
    (2, 2, 'Lost 20 pounds'),
    (3, 3, 'Completed 100 push-ups challenge');

-- Inserting data into the FitnessGoals table
INSERT INTO FitnessGoals (goalID, memberID, description) 
VALUES 
    (1, 1, 'Run 5 miles in under 30 minutes'),
    (2, 2, 'Achieve 15% body fat'),
    (3, 3, 'Squat double body weight');

-- Inserting data into the Routines table
INSERT INTO Routines (routineID, memberID, description) 
VALUES 
    (1, 1, 'Morning jog'),
    (2, 2, 'Weightlifting circuit'),
    (3, 3, 'Yoga practice');

-- Inserting data into the Session table
INSERT INTO Session (sessionID, memberID, trainerID, time, date, status) 
VALUES 
    (1, 1, 1, '08:00:00', '2024-04-10', 'Scheduled'),
    (2, 2, 2, '10:00:00', '2024-04-12', 'Completed'),
    (3, 3, 3, '15:00:00', '2024-04-15', 'Cancelled');

-- Inserting data into the FitnessClasses table
INSERT INTO FitnessClasses (classID, memberID, trainerID, time, date, status) 
VALUES 
    (1, 1, 1, '10:00:00', '2024-04-15', 'Scheduled'),
    (2, 2, 2, '12:00:00', '2024-04-17', 'Completed'),
    (3, 3, 3, '17:00:00', '2024-04-20', 'Cancelled');

-- Inserting data into the TrainerSchedule table
INSERT INTO TrainerSchedule (scheduleID, trainerID, time) 
VALUES 
    (1, 1, '08:00:00'),
    (2, 2, '10:00:00'),
    (3, 3, '15:00:00');

-- Inserting data into the Admin table
INSERT INTO Admin (adminID, loginID, firstname, lastname, phone) 
VALUES 
    (1, 7, 'Erik', 'Tenhag', '1234567890'),
    (2, 8, 'Pep', 'Guardiola', '9876543210');

-- Inserting data into the Rooms table
INSERT INTO Rooms (roomID, roomName) 
VALUES 
    (1, 'Yoga Room'),
    (2, 'Ball Room'),
    (3, 'Hype Room');

-- Inserting data into the Bookings table
INSERT INTO Bookings (bookingID, roomID, time) 
VALUES 
    (1, 1, '08:00:00'),
    (2, 2, '10:00:00'),
    (3, 3, '15:00:00');

-- Inserting data into the Equipments table
INSERT INTO Equipments (equipmentID, name, maintenanceDate) 
VALUES 
    (1, 'Treadmill', '2024-04-01'),
    (2, 'Dumbbells', '2024-04-05'),
    (3, 'Yoga Mats', '2024-04-10');

-- Inserting data into the BillPayment table
INSERT INTO BillPayment (billID, memberID, amount, paymentDate) 
VALUES 
    (1, 1, 50.00, '2024-04-01'),
    (2, 2, 75.00, '2024-04-05'),
    (3, 3, 100.00, '2024-04-10');

-- Time Availability
INSERT INTO Availability(availability_id, start_time, available_date, trainer_id)
VALUES
	(1, '10:00', '2024-04-23', 1),
	(2, '13:00', '2024-04-23', 1),
	(3, '9:00', '2024-04-26', 2),
	(4, '17:00', '2024-04-25', 3);