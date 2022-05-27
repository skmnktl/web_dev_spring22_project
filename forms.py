from libs import * 
from constants import *

# create new account
class AccountForm(FlaskForm):
	firstName      = StringField("First Name: ",  validators=[DataRequired()])
	lastName       = StringField("Last Name: ",   validators=[DataRequired()])
	email          = StringField("Email: ",       validators=[DataRequired()])
	accountID      = IntegerField("Account ID: ", validators=[DataRequired()])
	password       = StringField("Password: ",    validators=[DataRequired()])
	accountType    = RadioField("Account Type",   choices=[("S","Student"),("T","Teacher")])
	securityAnswer1 = StringField("Your Answer: ", validators=[DataRequired()])
	securityAnswer2 = StringField("Your Answer: ", validators=[DataRequired()])
	securityAnswer3 = StringField("Your Answer: ", validators=[DataRequired()])
	submit = SubmitField("Create Account")


# edit user information
class EditUserForm(FlaskForm):
	firstName      = StringField("First Name: ",  validators=[DataRequired()])
	lastName       = StringField("Last Name: ",   validators=[DataRequired()])
	email          = StringField("Email: ",       validators=[DataRequired()])
	accountID      = IntegerField("Account ID: ", validators=[DataRequired()])
	submit         = SubmitField("Edit User" , render_kw={"onclick": "editProfile()"})


# change password information
class ChangePasswordForm(FlaskForm):
	currPassword  = StringField("Current Password: ", validators=[DataRequired()])
	newPassword   = StringField("New Password: ",     validators=[DataRequired()])
	confPassword  = StringField("Confirm Password: ", validators=[DataRequired()])
	submit = SubmitField("Change Password", render_kw={"onclick": "changePassword()"})


# change password information
class GetEmailForm(FlaskForm):
	email = StringField("Enter Email: ", validators=[DataRequired(), Email()])
	submit = SubmitField("Sumbit Email")

class ForgotPasswordForm(FlaskForm):
	securityAnswer1 = StringField("Answer: ", 			validators=[DataRequired()])
	securityAnswer2 = StringField("Answer: ", 			validators=[DataRequired()])
	securityAnswer3 = StringField("Answer: ", 			validators=[DataRequired()])
	newPassword     = StringField("New Password: ",     validators=[DataRequired()])
	confNewPassword = StringField("Confirm Password: ", validators=[DataRequired()])
	submit = SubmitField("Reset Password", render_kw={"onclick": "resetPassword()"})

# edit questions
class EditQuestionsForm(FlaskForm):
    currPasswordQuestions    = StringField("Current Password: ", validators=[DataRequired()])
    # securityQuest1  = StringField("New Question 1: ", validators=[DataRequired()])
    # securityQuest2  = StringField("New Question 2: ", validators=[DataRequired()])
    # securityQuest3  = StringField("New Question 3: ", validators=[DataRequired()])
    securityAnswer1 = StringField("Your Answer: ", validators=[DataRequired()])
    securityAnswer2 = StringField("Your Answer: ", validators=[DataRequired()])
    securityAnswer3 = StringField("Your Answer: ", validators=[DataRequired()])
    submit = SubmitField("Change Questions")

class AnnouncementForm(FlaskForm):
	announcement = StringField("Announcement: ", widget=TextArea(), validators=[DataRequired()])
	submit = SubmitField("Create Announcement")

class AssignmentForm(FlaskForm):
	assignmentName = StringField("Assignment Name: ", validators=[DataRequired()])
	assignmentID =  IntegerField("Assignment ID: ", validators=[DataRequired()])
	assignmentDescription = StringField("Assignment Description: ", validators=[DataRequired()])
	numberOfPoints =  IntegerField("Number of Points: ", validators=[DataRequired()])
	dueDate = DateField("Due Date: ", validators=[DataRequired()])
	submit = SubmitField("Create Assignment")

class CourseForm(FlaskForm):
	courseName = StringField("Course Name: ", validators=[DataRequired()])
	courseDescription = StringField("Course Description: ", validators=[DataRequired()])
	courseCapacity = IntegerField("Course Capacity: ", validators=[DataRequired()])
	courseProfessor = StringField("Course Professor", validators=[DataRequired()])
	submit = SubmitField("Create Course")

class SubmitAssignmentForm(FlaskForm):
	assignmentSubmission = StringField("Submission: ", widget=TextArea(), validators=[DataRequired()])
	submit = SubmitField("Submit Assignment")

class GradeAssignmentForm(FlaskForm):
	assignmentGradeSubmission = IntegerField("Number of Points: ", validators=[DataRequired()])
	submit = SubmitField("Submit Grade")

class ActivateUserForm(FlaskForm):
	submit = SubmitField("Activate/Deactivate User")

class FilterUserForm(FlaskForm):
    status = StringField("Submission: ", validators=[DataRequired()])
    submit = SubmitField("status")

class AddToCourseForm(FlaskForm):
	submit = SubmitField("Add or Remove Student From Course")

class MyAccountForm(FlaskForm):
    userid = IntegerField("Assignment ID: ", validators=[DataRequired()])

class Login(FlaskForm):
	email     = StringField("Email: ",   validators=[DataRequired(), Email()])
	password  = StringField("Password: ",validators=[DataRequired()])
	submit	  = SubmitField("Login")
