-- User table
CREATE SEQUENCE user_login_seq;

CREATE TABLE UserLogin (
    loginID INT DEFAULT nextval('user_login_seq') PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Member table
CREATE SEQUENCE member_login_seq;

CREATE TABLE Member (
    memberID INT DEFAULT nextval('member_login_seq') PRIMARY KEY,
    loginID INT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(100),
    email VARCHAR(100),
    gender CHAR(1),
    age INT,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    FOREIGN KEY (loginID) REFERENCES UserLogin(loginID)
);

-- Trainer table
CREATE TABLE Trainer (
    trainerID INT PRIMARY KEY,
    loginID INT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    FOREIGN KEY (loginID) REFERENCES UserLogin(loginID)
);

-- TrainerMemberAccess table
CREATE TABLE TrainerViewMember (
    trainerID INT,
    memberID INT,
	PRIMARY KEY (trainerID, memberID),
    FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID),
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);


-- Achievements table
CREATE TABLE Achievements (
    achieveID INT PRIMARY KEY,
    memberID INT,
    achieveDescription TEXT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

-- FitnessGoals table
CREATE TABLE FitnessGoals (
    goalID INT PRIMARY KEY,
    memberID INT,
    description TEXT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

-- Routines table
CREATE TABLE Routines (
    routineID INT PRIMARY KEY,
    memberID INT,
    description TEXT,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE SEQUENCE session_id_seq;

-- Alter the Session table to use the sequence
CREATE TABLE Session (
    sessionID INT DEFAULT nextval('session_id_seq') PRIMARY KEY,
    memberID INT,
    trainerID INT,
    time TIME,
    date DATE,
    status VARCHAR(20),
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID)
);

-- FitnessClasses table
CREATE SEQUENCE class_id_seq;

CREATE TABLE FitnessClasses (
    classID INT PRIMARY KEY DEFAULT nextval('class_id_seq'),
    memberID INT,
    trainerID INT,
    time TIME,
    date DATE,
    status VARCHAR(20),
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID)
);

-- TrainerSchedule table
CREATE TABLE TrainerSchedule (
    scheduleID INT PRIMARY KEY,
    trainerID INT,
    time TIME,
    FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID)
);

-- Admin table
CREATE TABLE Admin (
    adminID INT PRIMARY KEY,
    loginID INT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    FOREIGN KEY (loginID) REFERENCES UserLogin(loginID)
);

-- Rooms table
CREATE TABLE Rooms (
    roomID INT PRIMARY KEY,
    roomName VARCHAR(50)
);

-- Bookings table
CREATE TABLE Bookings (
    bookingID INT PRIMARY KEY,
    roomID INT,
    time TIME,
    FOREIGN KEY (roomID) REFERENCES Rooms(roomID)
);

-- Equipments table
CREATE TABLE Equipments (
    equipmentID INT PRIMARY KEY,
    name VARCHAR(50),
    maintenanceDate DATE
);

-- BillPayment table
CREATE TABLE BillPayment (
    billID INT PRIMARY KEY,
    memberID INT,
    amount DECIMAL(10,2),
    paymentDate DATE,
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

--Time Availability
CREATE TABLE Availability (
    availability_id SERIAL PRIMARY KEY,
    start_time TIME NOT NULL,
    available_date DATE NOT NULL,
    trainer_id INT NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainerID)
);