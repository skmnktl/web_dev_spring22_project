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
    courseid = int(request.args['courseid'])
    params = {
        "courseid": courseid
    }
    response = json.loads(requests.get(apiUrls["getAssign"], params=params).text)
    print(response)
    if response["response"]:
        dataAssignments = []
        for d in response["data"].keys():
            dataAssignments.append(response["data"][d])
    else:
        dataAssignments = {}
        flash(response["error"])
        
    return render_template(
                            "assignments.html", 
                            headings = headingsAssignments, 
                            data     = dataAssignments,
                            courseid = courseid
                        )


@app.route(routeUrls["createAccount"], methods=["GET", "POST"])
def createAccount():
    if current_user.is_authenticated:
        # user is already logged in
        flash("User is already logged in!!")
        return redirect(url_for('tempDash'))
    print("CREATING ACCOUNT")
    form = AccountForm()
    firstName       = form.firstName.data
    lastName        = form.lastName.data
    accountID       = form.accountID.data
    email           = form.email.data
    password        = form.password.data
    accountType     = form.accountType.data
    securityAnswer1 = form.securityAnswer1.data
    securityAnswer2 = form.securityAnswer2.data
    securityAnswer3 = form.securityAnswer3.data

    if form.validate_on_submit():
        params = [
            ("firstname",firstName),
            ("lastname",lastName),
            ("username",email),
            ("accountType",accountType),
            ("password", generate_password_hash(password, method='sha256')),
            ("securityQuestions",f"{securityAnswer1}<|>{securityAnswer2}<|>{securityAnswer3}")
        ]
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
        securityAnswer3=securityAnswer3,
        securityQuestions = securityQuestions
    )


@app.route(routeUrls["createAssign"], methods=["GET", "POST"])
@login_required
def createAssign():
    form = AssignmentForm()
    assignmentName        = form.assignmentName.data
    assignmentID          = form.assignmentID.data
    assignmentDescription = form.assignmentDescription.data
    numberOfPoints        = form.numberOfPoints.data
    dueDate               = form.dueDate.data
    courseid              = int(request.args['courseid'])
    if form.validate_on_submit():
        # create a post request
        params = {
            "name": assignmentName,
            "description": assignmentDescription,
            "points": numberOfPoints,
            "duedate": dueDate,
            "courseid": courseid,
            "assignmentid": assignmentID
        }
        response = json.loads(requests.post(apiUrls["createAssign"], params=params).text)

        if response["response"]:
            flash("Assignment Added")
            return redirect(url_for('assignments', courseid=courseid))
        else:
            flash("Couldn't add the assignment")
            flash(response["error"])

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
    courseID = int(request.args['courseid'])
    if form.validate_on_submit():
        params={"message":announcement,"courseid":courseID}
        requests.post(apiUrls['createAnnouncement'],params=params)
        return "Created!"

    return render_template("createAnnouncement.html", announcement=announcement, form=form)

@app.route(routeUrls["announcements"])
def announcements():
    courseid = request.args['courseid']
    response = requests.get(apiUrls["getAnnouncements"],params = {"courseid":courseid})
    announcements = json.loads(response.text)
    return render_template("announcements.html", headings=headingsAnnouncements, data=dataAnnouncements, name=announcementCourseName, announcements=announcements,courseid=courseid)



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
            "courseprofessor": courseProfessor
        }
        response = requests.post(apiUrls["createCourse"], params=params)
        if json.loads(response.text):
            flash("Course Added")
        else:
            flash("Couldn't add the course")

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
    countActiveTeachers = json.loads(requests.get(backend + "/countactiveteachers").text)
    countActiveStudents = json.loads(requests.get(backend + "/countactivestudents").text)
    countCourses        = json.loads(requests.get(backend + "/countcourses").text)

    userSummary = [countActiveStudents,countActiveTeachers,countCourses]

    allUsers = json.loads(requests.get(backend+"/allusers").text)
    userData = []

    selection = 'all'
    for user in allUsers:
                if user['active'] == 1:
                    user['active'] = "active"
                else:
                    user['active'] = "inactive"
                userData.append(            [
                                user['userid'],
                                user['firstname'],
                                user['lastname'],
                                user['email'],
                                user['accountType'],
                                user['active']
                            ])



    # only if button is clicked
    if form.validate_on_submit():
        userid = request.form['rowUserID']
        params = {
            "userid":userid
        }

        response = json.loads(requests.post(backend + "/changeuserstatus", params=params).text)
        return render_template(
                    "adminDashboard.html",
                    headingsUserSummary=headingsUserSummary,
                    headingsUsers=headingsUsers,
                    dataUserSummary=userSummary,
                    status = "all",
                    dataUsers=userData,
                    form=form
                )

    return render_template("adminDashboard.html", headingsUserSummary=headingsUserSummary,
        headingsUsers=headingsUsers, dataUserSummary=userSummary,status=selection, dataUsers=userData, form=form)

@app.route(routeUrls["teacherDash"])
@login_required
def teacherDash():
    return render_template("teacherDashboard.html", headings=headingsDash, dataToGrade=dataDashTeacherToGrade)

@app.route(routeUrls["studentDash"])
@login_required
def studentDash():
    # get all the student assignments
    userid = int(request.args['userid'])
    params = {
        "userid": userid
    }

    # get all assignments
    response = json.loads(requests.get(apiUrls["getAllAssign"], params=params).text)
    print(response)
    dataDashStudentToDo = []
    dataDashStudentUpcoming = [] 
    dataDashStudentPastDue  = []
    if response["response"]:
        for d in response["data"].keys():
            data = response["data"][d]
            ass_date_type = datetime.strptime(data[-1], DATE_FORMAT).date() - datetime.today().date()
            if ass_date_type.days > 3:
                dataDashStudentToDo.append(data)
            elif ass_date_type.days < 0:
                dataDashStudentPastDue.append(data)
            else:
                dataDashStudentUpcoming.append(data)
    else:
        flash(response["error"])

    return render_template(
        "studentDashboard.html", 
        headings = headingsDash, 
        dataToDo     = dataDashStudentToDo, 
        dataUpcoming = dataDashStudentUpcoming, 
        dataPastDue  = dataDashStudentPastDue
    )

@app.route(routeUrls["tempDash"])
@login_required
def tempDash():
    userid = current_user.get_id()
    return render_template(
        "tempDashboard.html",
        userid = userid
    )

@app.route(routeUrls["editProfile"], methods=["GET", "POST"])
@login_required
def editProfile():
    editUserForm   = EditUserForm()
    changePassForm = ChangePasswordForm()
    editQuestForm  = EditQuestionsForm()

    firstName       = editUserForm.firstName.data
    lastName        = editUserForm.lastName.data
    email           = editUserForm.email.data
    accountID       = editUserForm.accountID.data

    currPassword = changePassForm.currPassword.data
    newPassword  = changePassForm.newPassword.data
    confPassword = changePassForm.confPassword.data

    currPasswordQuestions = editQuestForm.currPasswordQuestions.data
    # securityQuest1  = editQuestForm.securityQuest1.data
    # securityQuest2  = editQuestForm.securityQuest2.data
    # securityQuest3  = editQuestForm.securityQuest3.data
    securityAnswer1 = editQuestForm.securityAnswer1.data
    securityAnswer2 = editQuestForm.securityAnswer2.data
    securityAnswer3 = editQuestForm.securityAnswer3.data

    # edit user details
    if editUserForm.validate_on_submit():
        """
            userid INT unsigned NOT NULL AUTO_INCREMENT,
            password TEXT(256),
            email TEXT(256),
            accountType TEXT(3),
            securityQuestions VARCHAR(2000),
            firstname TEXT(256),
            lastname TEXT(256),
            active BOOLEAN,
            username CHAR(140), 
        """
        params = {
            "userid"  : current_user.get_id(),
            "property": "email",
            "value"   : email
        }

        resp = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

        params = {
            "userid"  : current_user.get_id(),
            "property": "username",
            "value"   : email
        }

        resp2 = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

        if resp["response"] and resp2["response"]:
            params = {
                "userid"  : current_user.get_id(),
                "property": "firstname",
                "value"   : firstName
            }

            resp = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

            if resp["response"]:
                params = {
                    "userid"  : current_user.get_id(),
                    "property": "lastname",
                    "value"   : lastName
                }

                resp = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

                if resp["response"]:
                    flash("Details Updated")
                else:
                    flash(resp["error"])
            else:
                flash(resp["error"])
        else:
            flash(resp["error"])

    # edit password details
    if changePassForm.validate_on_submit():
        # verify pass
        params = {
            "userid"  : current_user.get_id(),
            "password": currPassword
        }
        resp = json.loads(requests.get(apiUrls["verifyPass"], params = params).text)

        if resp["response"]:
            if newPassword == confPassword:
                # updatepassword
                params = {
                    "userid"  : current_user.get_id(),
                    "property": "password",
                    "value"   : generate_password_hash(newPassword, method='sha256')
                }

                resp = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

                if resp["response"]:
                    flash("Password Updated!!")
                else:
                    flash(resp["error"])
            else:
                flash("New Passwords don't Match")
        else:
            flash("Incorrect Password")

    # edit questions details
    if editQuestForm.validate_on_submit():
        # verify pass
        params = {
            "userid"  : current_user.get_id(),
            "password": currPasswordQuestions
        }
        resp = json.loads(requests.get(apiUrls["verifyPass"], params = params).text)

        if resp["response"]:
            params = {
                "userid"  : current_user.get_id(),
                "property": "securityQuestions",
                "value"   : "<|>".join([
                                securityAnswer1, 
                                securityAnswer2, 
                                securityAnswer3
                            ])
            }

            resp = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

            if resp["response"]:
                flash("Details Updated")
            else:
                flash(resp["error"])
        else:
            flash("Incorrect Password")


    # if not submit validated or new page
    return render_template(
        "editProfile.html",
        editUserForm=editUserForm,
        changePasswordForm = changePassForm,
        editQuestionsForm = editQuestForm,
        firstName=firstName,
        lastName=lastName,
        email=email,
        accountID = accountID,
        currPassword=currPassword,
        newPassword=newPassword,
        confPassword = confPassword,
        currPasswordQuestions = currPasswordQuestions,
        # securityQuest1=securityQuest1,
        # securityQuest2=securityQuest2,
        # securityQuest3=securityQuest3,
        securityQuestions = securityQuestions,
        securityAnswer1=securityAnswer1,
        securityAnswer2=securityAnswer2,
        securityAnswer3=securityAnswer3,
    )


@app.route(routeUrls["forgotPassword"], methods=["GET", "POST"])
def forgotPassword():
    if current_user.is_authenticated:
        # user is already logged in
        flash("User is already logged in!!")
        return redirect(url_for('tempDash'))
    
    form = GetEmailForm()
    email = form.email.data
    params = {
        "email": email
    }

    if form.validate_on_submit():
        # verify user
        response = json.loads(requests.get(apiUrls["verifyuser"], params=params).text)

        if response["response"]:
            return redirect(url_for('forgotPasswordForm', userid = response["userid"], email = email))
        else:
            flash("User doesn't exist!!!")


    return render_template(
        "forgotPassword.html",
        form = form,
        email = email
    )


@app.route(routeUrls["forgotPassForm"], methods=["GET", "POST"])
def forgotPasswordForm():
    if current_user.is_authenticated:
        # user is already logged in
        flash("User is already logged in!!")
        return redirect(url_for('tempDash'))

    form = ForgotPasswordForm()
    try:
        email  = request.args["email"]
        userid = int(request.args["userid"])
        params = {
            "email": email
        }
    except:
        return redirect(url_for('forgotPassword'))
    
    securityAnswer1 = form.securityAnswer1.data
    securityAnswer2 = form.securityAnswer2.data
    securityAnswer3 = form.securityAnswer3.data
    newPass         = form.newPassword.data
    confNewPass     = form.confNewPassword.data
    
    if form.validate_on_submit():
        # get all the answers
        securityAnswers = json.loads(requests.get(apiUrls["getQuestions"], params=params).text)
        if  securityAnswer1 == securityAnswers[0]\
        and securityAnswer2 == securityAnswers[1]\
        and securityAnswer3 == securityAnswers[2]:
            if confNewPass == newPass:
                #updatepassword
                params = {
                    "userid"  : userid,
                    "property": "password",
                    "value"   : generate_password_hash(newPass, method='sha256')
                }

                resp = json.loads(requests.post(apiUrls["updateUserData"], params = params).text)

                if resp["response"]:
                    flash("Password Updated!!")
                    return redirect(url_for("auth.login"))
                else:
                    flash(resp["error"])
            else:
                flash("Passwords doesn't match")
        else:
            flash("Incorrect Answers")      

    return render_template(
            "forgotPasswordForm.html",
            form = form,
            securityAnswer1 = securityAnswer1,
            securityAnswer2 = securityAnswer2,
            securityAnswer3 = securityAnswer3,
            newPassword     = newPass, 
            confNewPassword = confNewPass,
            securityQuestions = securityQuestions
        )

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
    userid = request.args['userid']
    userData = json.loads(requests.get(backend+"/getuser",params={"userid":userid}).text)
    courseData = json.loads(requests.get(backend+"/getallcourseidswithcapacity").text)
    courses = []
    for course in courseData:
        courses.append(course.values())
        print(course.values())
    if form.validate_on_submit():
        coursedata = request.form['rowCourseID']
        courseid = int(coursedata[13:-2].split(",")[0])
        requests.post(backend+"/addremovestudentcourse",params={"courseid":courseid,"student":userid})
    # edit db
    return render_template(
                            "addToCourse.html", 
                            headings = headingsAddToCourse, 
                            data = courses,
                            firstName = userData['firstname'],
                            lastName = userData['lastname'],
                            email = userData['email'],
                            form = form
                        )

@app.route(routeUrls["myAccount"],methods=["GET","POST"])
@login_required
def myAccount():
    form = MyAccountForm()
    userid = request.args
    user = json.loads(requests.get(backend+"/getuser",params={"userid":current_user.get_id()}).text)
    return render_template(
                                "myAccount.html",
                                userData = user,
                                userid = user['userid'],
                                firstname = user['firstname'],
                                lastname = user['lastname'],
                                email = user['email'],
                                headings = ["User ID","First Name", "Last Name", "Email"]
                            )
# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),


    
