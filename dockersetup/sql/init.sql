USE db;

CREATE TABLE user (
	id INT unsigned NOT NULL AUTO_INCREMENT,
	password TEXT(256),
	email TEXT(256),
	accountType TEXT(3),
	securityQuestions VARCHAR(2000),
	firstname TEXT(256),
	lastname TEXT(256),
    active BOOLEAN,
    username TEXT(256),
    PRIMARY KEY (id)
);

CREATE TABLE `course` (
	id INT unsigned NOT NULL AUTO_INCREMENT,
	coursename TEXT(256),
	coursedescription VARCHAR(2000),
	coursecapacity INT,
	professor TEXT(256),
	students VARCHAR(2000),
	announcementInbox VARCHAR(2000),
    PRIMARY KEY (id)

);

CREATE TABLE assignment (
	id INT unsigned NOT NULL,
    name TEXT(256),
    description VARCHAR(2000),
    points INT,
    duedate DATE,
    courseid INT unsigned,
    student INT unsigned,
    PRIMARY KEY (courseid, id, student)
);

CREATE TABLE announcements (
    message VARCHAR(2000),
    senddate DATE,
    course INT
);

