"""
    This file holds all the constants to be used
"""
from libs import *

# routing urls
routeUrls = {
    "main"   : "/", 
    "login"  : "/login",
    "logout" : "/logout",
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
    ("Final project","Build a website","100","5//2021")
)

headingsGrades = ("Assignment Name","Number of Points","Grade")
dataGrades = (
    ("Midterm project","100","97"),
    ("Midterm project","100","97"),
    ("Midterm project","100","97")
)

headingsUserSummary = ("Number of Active Students","Number of Active Teachers","Number of Courses")
dataUserSummary = ("67","3","5")

headingsUsers = ("ID","First Name","Last Name","Email","Account Type","Active Status","Actions")
dataUsers = (
    ("22","Jeff","Smith","jsmith@aol.com","Student","Active"),
    ("18","Jeff","Jones","jjones@aol.com","Student","Inactive"),
    ("16","Jeff","Johnson","jjohns@aol.com","Teacher","Active"),
)

headingsGradeAssignment = ("ID","Student First Name","Student Last Name","Student Email", "Submit Grade")
dataGradeAssignment = (
    ("14","Jeff","Smith","jsmith@aol.com"),
    ("15","Jeff","Smith","jsmith@aol.com"),
    ("16","Jeff","Smith","jsmith@aol.com")
)

assignmentName = ("Final project")
assignmentDescription = ("Build a website")

firstNameAddToCourse = ("Jeff")
lastNameAddToCourse = ("Smith")
emailAddToCourse = ("jsmith@gmail.com")
headingsAddToCourse = ("ID","Course Name","Course Description","Course Capacity","Professor","Actions")
dataAddToCourse = (
    ("145","Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("146","Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("147","Intro to Web Dev","An introductory web course","50","Prof. Jones")
)

assignmentGradeName = ("Midterm project")




## create app
def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return 12
    
    # db.init_app(app)
    # sets autoreload on changes    
    app.run(debug=True)
    app.config['SECRET_KEY'] = SECRET_KEY

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app