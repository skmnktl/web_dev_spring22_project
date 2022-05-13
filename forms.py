from libs import * 
from constants import *

# create new account
class AccountForm(FlaskForm):
	firstName      = StringField("First Name: ",  validators=[DataRequired()])
	lastName       = StringField("Last Name: ",   validators=[DataRequired()])
	email          = StringField("Email: ",       validators=[DataRequired(), Email()])
	accountID      = IntegerField("Account ID: ", validators=[DataRequired()])
	password       = StringField("Password: ",    validators=[DataRequired()])
	accountType    = RadioField("Account Type",   choices=[("student","Student"),("teacher","Teacher")])
	securityAnswer1 = StringField("Your Answer: ", validators=[DataRequired()])
	securityAnswer2 = StringField("Your Answer: ", validators=[DataRequired()])
	securityAnswer3 = StringField("Your Answer: ", validators=[DataRequired()])
	submit = SubmitField("Create Account")

# edit user information
class EditUserForm(FlaskForm):
	firstName      = StringField("First Name: ",  validators=[DataRequired()])
	lastName       = StringField("Last Name: ",   validators=[DataRequired()])
	accountID      = IntegerField("Account ID: ", validators=[DataRequired()])
	submit = SubmitField("Edit User")

# change password information
class ChangePasswordForm(FlaskForm):
    currPassword    = StringField("Current Password: ", validators=[DataRequired()])
    newPassword     = StringField("New Password: ",     validators=[DataRequired()])
    confNewPassword = StringField("Confirm Password: ", validators=[DataRequired()])
    submit = SubmitField("Change Password")

class AnnouncementForm(FlaskForm):
	announcement = StringField("Announcement: ", widget=TextArea(), validators=[DataRequired()])
	submit = SubmitField("Create Announcement")

class AssignmentForm(FlaskForm):
	assignmentName = StringField("Assignment Name: ", validators=[DataRequired()])
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