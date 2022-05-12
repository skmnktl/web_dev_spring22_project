"""
    This file holds all the constants to be used
"""

# routing urls
routeUrls = {
    "main"   : "/", 
    "login"  : "/login",
    "courses": "/courses",
    "grades" : "/grades",
    "addToCourse"   : "/addtocourse",
    "assignments"   : "/assignments",
    "announcements" : "/announcements",
    "createAccount" : "/newaccount",
    "createAssign"  : "/newassign",
    "createAnnounce" : "/newannounce",
    "createCourse"  : "/newcourse",
    "adminDash"     : "/admindash",
    "teacherDash"   : "/teacherdash",
    "studentDash"   : "/studentdash",
    "tempDash"      : "/tempdash",
    "editProfile"   : "/editprofile",
    "forgotPassword": "/forgotpass",
    "gradeAssign"   : "/gradeassign",
    "submitAssign"  : "/submitassign",
}

# secret key
SECRET_KEY = "web_dev_team"

headingsCourses = ("Course Name","Course Description","Course Capacity","Professor")
dataCourses = (
	("Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("Intro to Web Dev","An introductory web course","50","Prof. Jones")
	)

headingsAnnouncements = ("Announcement","Date")
dataAnnouncements = (
    ("New assignment posted","5/7/2021"),
    ("New assignment posted","5/7/2021"),
    ("New assignment posted","5/7/2021")
)

headingsAssignments = ("Assignment Name","Assignment Description","Number of Points","Due Date","Actions")
dataAssignments = (
    ("Final project","Build a website","100","5/21/2021"),
    ("Final project","Build a website","100","5/21/2021"),
    ("Final project","Build a website","100","5/21/2021")
)

headingsDash = ("Assignment Name","Assignment Description","Number of Points","Due Date")
dataDashStudentToDo = (
    ("Final project","Build a website","100","5/12/2021"),
    ("Final project","Build a website","100","5/12/2021"),
    ("Final project","Build a website","100","5/12/2021")
)
dataDashStudentUpcoming = (
    ("Final project","Build a website","100","5/21/2021"),
    ("Final project","Build a website","100","5/21/2021"),
    ("Final project","Build a website","100","5/21/2021")
)
dataDashStudentPastDue = (
    ("Final project","Build a website","100","5/1/2021"),
    ("Final project","Build a website","100","5/1/2021"),
    ("Final project","Build a website","100","5/1/2021")
)
dataDashTeacherToGrade = (
    ("Final project","Build a website","100","5/9/2021"),
    ("Final project","Build a website","100","5/9/2021"),
    ("Final project","Build a website","100","5/9/2021")
)

account_type = {'samrodman@mac.com':'admin','samrodman@mac.com':'student','srodman1@chicagobooth.edu':'teacher'}
