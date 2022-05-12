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

headings = ("Course Name","Course Description","Course Capacity","Professor")
data = (
	("Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("Intro to Web Dev","An introductory web course","50","Prof. Jones")
	)
account_type = {'samrodman@mac.com':'admin','samrodman@mac.com':'student','srodman1@chicagobooth.edu':'teacher'}
