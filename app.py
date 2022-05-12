from libs import * 
from constants import *


# sets autoreload on changes    
app.run(debug=True)
app.config['SECRET_KEY'] = SECRET_KEY

# sample :removeit
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

class AnnouncementForm(FlaskForm):
	announcement = StringField("Announcement", widget=TextArea(), validators=[DataRequired()])
	submit = SubmitField("Create Announcement")

class AssignmentForm(FlaskForm):
	assignmentName = StringField("Assignment Name", validators=[DataRequired()])
	assignmentDescription = StringField("Assignment Description", validators=[DataRequired()])
	numberOfPoints =  IntegerField("Number of Points", validators=[DataRequired()])
	dueDate = StringField("Due Date", validators=[DataRequired()])
	submit = SubmitField("Create Assignment")

class AccountForm(FlaskForm):
	firstName = StringField("First Name:", validators=[DataRequired()])
	lastName = StringField("Last Name:", validators=[DataRequired()])
	email = StringField("Email:", validators=[DataRequired()])
	accountID = IntegerField("Account ID:", validators=[DataRequired()])
	password = StringField("Password:", validators=[DataRequired()])

	accountType = RadioField("Account Type", choices=[("student","Student"),("teacher","Teacher")])

	securityAnswer1 = StringField("Your Answer:", validators=[DataRequired()])
	securityAnswer2 = StringField("Your Answer:", validators=[DataRequired()])
	securityAnswer3 = StringField("Your Answer:", validators=[DataRequired()])

	submit = SubmitField("Create Account")


# http://127.0.0.1:5000/
@app.route(routeUrls["main"])
def home():
    return "Hello, Flask!"

@app.route(routeUrls["login"])
def login():
	return render_template("login.html")

@app.route(routeUrls["courses"])
def courses():
	return render_template("courses.html",headings=headingsCourses,data=dataCourses)

# http://127.0.0.1:5000/grades
@app.route(routeUrls["grades"])
def grades():
	return render_template("grades.html")


@app.route(routeUrls["assignments"])
def assignments():
	return render_template("assignments.html",headings=headingsAssignments,data=dataAssignments)


@app.route(routeUrls["announcements"])
def announcements():
	return render_template("announcements.html",headings=headingsAnnouncements,data=dataAnnouncements)


@app.route(routeUrls["createAccount"])
def createAccount():
	firstName = None
	lastName = None
	email = None
	accountID = None
	password = None
	accountType = None

	securityAnswer1 = None
	securityAnswer2 = None
	securityAnswer3 = None
	form = AccountForm()

	return render_template("createAccount.html",form=form,firstName=firstName,lastName=lastName,email=email,accountID=accountID,password=password,accountType=accountType,securityAnswer1=securityAnswer1,securityAnswer2=securityAnswer2,securityAnswer3=securityAnswer3)


@app.route(routeUrls["createAssign"])
def createAssign():
	return render_template("createAssignment.html")


@app.route(routeUrls["createAnnounce"],methods=["GET","POST"])
def createAnnounce():
	announcement = None
	form = AnnouncementForm()

	if form.validate_on_submit():
		announcement = form.announcement.data
		form.announcement.data = ""
	
	return render_template("createAnnouncement.html",announcement=announcement,form=form)

@app.route(routeUrls["createCourse"])
def createCourse():
	return render_template("createCourse.html")

@app.route(routeUrls["adminDash"])
def adminDash():
	return render_template("adminDashboard.html")

@app.route(routeUrls["teacherDash"])
def teacherDash():
	return render_template("teacherDashboard.html",headings=headingsDash,dataToGrade=dataDashTeacherToGrade)

@app.route(routeUrls["studentDash"])
def studentDash():
	return render_template("studentDashboard.html",headings=headingsDash,dataToDo=dataDashStudentToDo,dataUpcoming=dataDashStudentUpcoming,dataPastDue=dataDashStudentPastDue)

@app.route(routeUrls["tempDash"])
def tempDash():
	return render_template("tempDashboard.html")

@app.route(routeUrls["editProfile"])
def editProfile():
	return render_template("editProfile.html")

@app.route(routeUrls["forgotPassword"])
def forgotPassword():
	return render_template("forgotPassword.html")

@app.route(routeUrls["submitAssign"])
def submitAssign():
	return render_template("submitAssignment.html")

@app.route(routeUrls["gradeAssign"])
def gradeAssign():
	return render_template("gradeAssignment.html")

@app.route(routeUrls["addToCourse"])
def addToCourse():
	return render_template("addToCourse.html")

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 

