CREATE TABLE `user` (
	`id` INT unsigned NOT NULL AUTO_INCREMENT PRIMARY_KEY,
	`password` TEXT,
	`email` TEXT DEFAULT '',
	`accountType` TEXT,
	`securityQuestions` VARCHAR,
	`firstname` VARCHAR,
	`lastname` VARCHAR
);

CREATE TABLE `course` (
	`id` INT unsigned NOT NULL AUTO_INCREMENT PRIMARY_KEY,
	`coursename` TEXT,
	`coursedescription` VARCHAR,
	`coursecapacity` INT,
	`professor` TEXT,
	`students` VARCHAR DEFAULT '',
	`self.announcementInbox` VARCHAR DEFAULT ''
);

CREATE TABLE `assignment`{
    `name` TEXT,
    `descriptoin` VARCHAR,
    `points` INT,
    `duedate` DATE,
    `courseid` INT unsigned
};

CREATE TABLE `announcements` {
    `message` VARCHAR,
    `date` DATE,
    `course` INT
}

