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


# http://127.0.0.1:5000/
@app.route(routeUrls["main"])
def home():
    return "Hello, Flask!"

@app.route(routeUrls["login"])
def login():
	return render_template("login.html")

@app.route(routeUrls["courses"])
def courses():
	return render_template("courses.html",headings=headings,data=data)


# http://127.0.0.1:5000/grades
@app.route(routeUrls["grades"])
def grades():
	return render_template("grades.html")


@app.route(routeUrls["assignments"])
def assignments():
	return render_template("assignments.html")


@app.route(routeUrls["announcements"])
def announcements():
	return render_template("announcements.html")


@app.route(routeUrls["createAccount"])
def createAccount():
	return render_template("createAccount.html")


@app.route(routeUrls["createAssign"])
def createAssign():
	return render_template("createAssignment.html")


@app.route(routeUrls["createAnnounce"])
def createAnnounce():
	return render_template("createAnnouncement.html")


@app.route(routeUrls["createCourse"])
def createCourse():
	return render_template("createCourse.html")

@app.route(routeUrls["adminDash"])
def adminDash():
	return render_template("adminDashboard.html")

@app.route(routeUrls["teacherDash"])
def teacherDash():
	return render_template("teacherDashboard.html")

@app.route(routeUrls["studentDash"])
def studentDash():
	return render_template("studentDashboard.html")

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

# @app.route(routeUrls["createCourse"])
# def createCourse():
# 	return render_template("createCourse.html")

# # http://127.0.0.1:5000/createAnnouncement.html
# @app.route("/createAnnouncement.html",methods=["GET","POST"])
# def createAnnouncement():
# 	announcement = None
# 	form = AnnouncementForm()

# 	#Validate form
# 	if form.validate_on_submit():
# 		announcement = form.announcement.data
# 		form.announcement.data = ""

	
# 	return render_template("createAnnouncement.html", announcement=announcement, form=form)

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 

