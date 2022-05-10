from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "web_dev_team"

headings = ("Course Name","Course Description","Course Capacity","Professor")
data = (
	("Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("Intro to Web Dev","An introductory web course","50","Prof. Jones"),
	("Intro to Web Dev","An introductory web course","50","Prof. Jones")
	)
account_type = {'samrodman@mac.com':'admin','samrodman@mac.com':'student','srodman1@chicagobooth.edu':'teacher'}

# Create a Form Class
class AnnouncementForm(FlaskForm):
	announcement = StringField("Announcement", widget=TextArea(), validators=[DataRequired()])
	submit = SubmitField("Create Announcement")

# create a route decorator
@app.route("/")
def index():
	return "<h1>Hello world</h1>"



# http://127.0.0.1:5000/user/<name>
@app.route('/user/<name>')
def user(name):
	return render_template("user.html", user_name=name)


# http://127.0.0.1:5000/courses.html
@app.route("/courses.html")
def courses():
	return render_template("courses.html",headings=headings,data=data)


# http://127.0.0.1:5000/grades.html
@app.route("/grades.html")
def grades():
	return render_template("grades.html")

# http://127.0.0.1:5000/accouncements.html
@app.route("/announcements.html")
def announcements():
	return render_template("announcements.html")

# http://127.0.0.1:5000/createAnnouncement.html
@app.route("/createAnnouncement.html",methods=["GET","POST"])
def createAnnouncement():
	announcement = None
	form = AnnouncementForm()

	#Validate form
	if form.validate_on_submit():
		announcement = form.announcement.data
		form.announcement.data = ""

	
	return render_template("createAnnouncement.html", announcement=announcement, form=form)

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 


