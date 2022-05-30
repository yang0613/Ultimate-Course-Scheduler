DROP SCHEMA IF EXISTS Majors CASCADE;
CREATE SCHEMA Majors;

ALTER ROLE CURRENT_USER SET SEARCH_PATH TO Majors;

DROP TABLE IF EXISTS Classes;
CREATE TABLE Classes(
    classID VARCHAR(10),
    className TEXT NOT NULL,
    subject TEXT NOT NULL,
    credit INTEGER NOT NULL,
    diffculty INTEGER,
    quarters VARCHAR(50),
    instructor TEXT,
    PRIMARY KEY (classID)
);

DROP TABLE IF EXISTS Requirements;
CREATE TABLE Requirements(
    classID VARCHAR(10),
    preReq TEXT,
    GradReq TEXT NOT NULL,
    PRIMARY KEY (classID),
    FOREIGN KEY (classID) REFERENCES Classes
);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    username VARCHAR(20),
    password VARCHAR(20) NOT NULL,
    academicPlan jsonb,
    PRIMARY KEY (username)
);


