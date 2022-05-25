from libs import *
from constants import *
from forms import *

app = create_app()

@app.route(routeUrls["courses"])
@login_required
def courses():
    #fetch all the course ids
    response = requests.get(apiUrls["getCourseIds"])
    courses = []
    courseids = json.loads(json.loads(response.text))
    # appedn all the courses
    for courseid in courseids['courseids']:
        response = requests.get(apiUrls["getCourse"],
                                params={
                                    "courseid":int(courseid)
                                })
        courses.append(json.loads(json.loads(response.text)))
    


    return render_template(
                            "courses.html", 
                            headings = headingsCourses,
                            data = dataCourses, 
                            courses = courses
                        )


@app.route(routeUrls["grades"])
@login_required
def grades():
    return render_template("grades.html", headings=headingsGrades, data=dataGrades)


@app.route(routeUrls["assignments"])
@login_required
def assignments():
    return render_template("assignments.html", headings=headingsAssignments, data=dataAssignments)


@app.route(routeUrls["announcements"])
def announcements():
    courseid = request.args['courseid']
    response = requests.get(apiUrls["getAnnouncements"],params = {"courseid":courseid})
    announcements = json.loads(response.text)
    return render_template("announcements.html", headings=headingsAnnouncements, data=dataAnnouncements, name=announcementCourseName, announcements=announcements)


@app.route(routeUrls["createAccount"], methods=["GET", "POST"])
def createAccount():
    if current_user.is_authenticated:
        # user is already logged in
        flash("User is already logged in!!")
        return redirect(url_for('tempDash'))
    print("CREATING ACCOUNT")
    form = AccountForm()
    firstName = form.firstName.data
    lastName  = form.lastName.data
    accountID  = form.accountID.data
    email     = form.email.data
    password  = form.password.data
    accountType = form.accountType.data
    securityAnswer1 = ""
    securityAnswer2 = ""
    securityAnswer3 = ""

    if form.validate_on_submit():
        params = [("firstname",firstName),
                  ("lastname",lastName),
                  ("username",email),
                  ("accountType",accountType),
                  ("password", generate_password_hash(password, method='sha256')),
                  ("securityQuestions",f"Q1<|>{securityAnswer1}Q2<|>{securityAnswer2}Q3<|>{securityAnswer3}")]
        params = dict(params)
        response = requests.post(apiUrls["createUser"], params=params)
        return redirect(url_for('auth.login'))

    # if not submit validated or new page
    return render_template(
                        "createAccount.html",
                        form=form,
                        firstName=firstName,
                        lastName=lastName,
                        email=email,
                        accountID = accountID,
                        password=password,
                        accountType=accountType,
                        securityAnswer1=securityAnswer1,
                        securityAnswer2=securityAnswer2,
                        securityAnswer3=securityAnswer3)

@app.route(routeUrls["createAssign"], methods=["GET", "POST"])
@login_required
def createAssign():
    form = AssignmentForm()
    assignmentName        = form.assignmentName.data
    assignmentID        = form.assignmentID.data
    assignmentDescription = form.assignmentDescription.data
    numberOfPoints        = form.numberOfPoints.data
    dueDate               = form.dueDate.data

    if form.validate_on_submit():
        # create a post request
        params = {
            "name": assignmentName,
            "description": assignmentDescription,
            "points": numberOfPoints,
            "duedate": dueDate,
            "courseid": "TODO",
            "assignmentid": 10000
        }
        response = requests.post(apiUrls["createAssign"], params=params)

        if json.loads(response.text):
            flash("Assignment Added")
        else:
            flash("Couldn't add the assignment")
    else:
        flash("Invalid Enteries!")

    return render_template("createAssignment.html", 
                            form=form, 
                            assignmentName=assignmentName, 
                            assignmentID=assignmentID, 
                            assignmentDescription=assignmentDescription, 
                            numberOfPoints=numberOfPoints, 
                            dueDate=dueDate)


@app.route(routeUrls["createAnnounce"],methods=["GET","POST"])
@login_required
def createAnnounce():
    form = AnnouncementForm()
    announcement = form.announcement.data
    courseID = request.args['courseid']
    if form.validate_on_submit():
        request.post(routeUrls['createAnnouncement'],params={"message":announcement,"courseid":courseid})
        courseid = request.args['courseid']
        response = requests.get(apiUrls["getAnnouncements"],params = {"courseid":courseid})
        announcements = json.loads(response.text)
        #return render_template("courses.html", headings=headingsAnnouncements, data=dataAnnouncements, name=announcementCourseName, announcements=announcements)

    return render_template("createAnnouncement.html", announcement=announcement, form=form)


@app.route(routeUrls["createCourse"],methods=["GET","POST"])
@login_required
def createCourse():
    form = CourseForm()
    courseName        = form.courseName.data
    courseDescription = form.courseDescription.data
    courseCapacity    = form.courseCapacity.data
    courseProfessor   = form.courseProfessor.data
    

    if form.validate_on_submit():
        params = {
            "coursename": courseName,
            "coursedescription": courseDescription,
            "coursecapacity": courseCapacity,
            "professor": courseProfessor
        }
        response = requests.post(apiUrls["createCourse"], params=params)
        if json.loads(response.text):
            flash("Course Added")
        else:
            flash("Couldn't add the course")
    else:
        flash("Invalid Enteries!")

    return render_template("createCourse.html", 
                    form=form, 
                    courseName=courseName, 
                    courseDescription=courseDescription, 
                    courseCapacity=courseCapacity, 
                    courseProfessor=courseProfessor)

@app.route(routeUrls["adminDash"],methods=["GET","POST"])
@login_required
def adminDash():
    form = ActivateUserForm()

    if form.validate_on_submit():
        userID = "55" # passed in from table
    # edit db

    return render_template("adminDashboard.html", headingsUserSummary=headingsUserSummary, headingsUsers=headingsUsers, dataUserSummary=dataUserSummary, dataUsers=dataUsers, form=form)

@app.route(routeUrls["teacherDash"])
@login_required
def teacherDash():
    return render_template("teacherDashboard.html", headings=headingsDash, dataToGrade=dataDashTeacherToGrade)

@app.route(routeUrls["studentDash"])
@login_required
def studentDash():
    return render_template("studentDashboard.html", headings=headingsDash, dataToDo=dataDashStudentToDo, dataUpcoming=dataDashStudentUpcoming, dataPastDue=dataDashStudentPastDue)

@app.route(routeUrls["tempDash"])
@login_required
def tempDash():
    return render_template("tempDashboard.html")

@app.route(routeUrls["editProfile"])
@login_required
def editProfile():
    return render_template("editProfile.html")

@app.route(routeUrls["forgotPassword"])
def forgotPassword():
    return render_template("forgotPassword.html")

@app.route(routeUrls["submitAssign"],methods=["GET","POST"])
@login_required
def submitAssign():
    assignmentSubmission = None
    form = SubmitAssignmentForm()

    if form.validate_on_submit():
        # write to db
        pass
    return render_template("submitAssignment.html", form=form, assignmentSubmission=assignmentSubmission, name=assignmentName, description=assignmentDescription)

@app.route(routeUrls["gradeAssign"],methods=["GET","POST"])
@login_required
def gradeAssign():
    assignmentGradeSubmission = None
    form = GradeAssignmentForm()

    if form.validate_on_submit():
        studentID = "55" # passed from table
        assignmentID = "55" # passed from url
    # edit db
    return render_template("gradeAssignment.html", headings=headingsGradeAssignment, data=dataGradeAssignment, assignmentGradeSubmission=assignmentGradeSubmission, form=form, name=assignmentGradeName)

@app.route(routeUrls["addToCourse"],methods=["GET","POST"])
@login_required
def addToCourse():
    form = AddToCourseForm()

    if form.validate_on_submit():
        userID = "55" # passed in from url
        assignmentID = "55" # passed in from table
    # edit db
    return render_template(
                            "addToCourse.html", 
                            headings = headingsAddToCourse, 
                            data = dataAddToCourse, 
                            firstName = firstNameAddToCourse, 
                            lastName = lastNameAddToCourse, 
                            email = emailAddToCourse, 
                            form = form
                        )

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),


    