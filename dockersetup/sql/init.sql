USE db;

CREATE TABLE user (
    userid INT unsigned NOT NULL AUTO_INCREMENT,
	password TEXT(256),
	email TEXT(256),
	accountType TEXT(3),
    securityQuestions VARCHAR(2000),
	firstname TEXT(256),
	lastname TEXT(256),
    active BOOLEAN,
    username CHAR(140),
    PRIMARY KEY (userid, username)
);

CREATE TABLE `course` (
	courseid INT unsigned NOT NULL AUTO_INCREMENT,
	coursename CHAR(140),
	coursedescription VARCHAR(2000),
	coursecapacity INT,
	professor TEXT(256),
	students VARCHAR(2000),
	announcementInbox VARCHAR(2000),
    PRIMARY KEY (courseid, coursename)

);

CREATE TABLE assignment (
	assignmentid INT unsigned NOT NULL,
    name TEXT(256),
    description VARCHAR(2000),
    points INT,
    duedate DATE,
    courseid INT unsigned,
    student INT unsigned,
    PRIMARY KEY (courseid, assignmentid, student)
);

CREATE TABLE announcements (
    announcementid INT unsigned NOT NULL AUTO_INCREMENT,
    message VARCHAR(2000),
    senddate DATE,
    courseid INT,
    PRIMARY KEY (announcementid)
);


CREATE TABLE loggedIn (
    userid INT unsigned NOT NULL,
	password TEXT(256),
	email TEXT(256),
    PRIMARY KEY (userid)
);