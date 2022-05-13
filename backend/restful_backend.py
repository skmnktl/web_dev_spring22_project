import crud
import json
from random import choice
from datetime import date
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

USER_FIELDS = ['password','email','accountType','securityQuestions','firstname','lastname','username','active']


class CreateUser(Resource):

    def __init__(self,accountType, password, username, securityQuestions, firstname, lastname):
        User.createUser(accountType, password, username, securityQuestions, firstname, lastname)
        return "success"


class User():

    @staticmethod
    def createUser(accountType, password, username, securityQuestions, firstname, lastname):
        self.accountType = accountType
        self.password = password
        self.username = username
        self.email = username
        self.firstname = firstname
        self.lastname = lastname
        self.securityQuestions = json.dumps(securityQuestions)
        self.active = True
        
        values = [self.password, self.email, self.accountType, self.securityQuestions, self.firstname, self.lastname, self.username, self.active]
        try:
            crud.batch_update("user", "username",username,USER_FIELDS,values)
            return "success"
        except:
            return "failure"

    @staticmethod
    def isUsernameUnique(username) -> bool:
        load = crud.read("user","username",username,["username"])
        return {"value":load}    
    
    @staticmethod
    def getUserInfo(username):
        row = crud.read("user","username",username)
        return {"value" : row}
    
    @staticmethod
    def changeUserData(username, field, newValue):
        if field == "securityQuestions":
            return "wrong method called; edit failed"
        else:
            try:
                crud.update("user",'username',username, field, newValue)
                return "success"
            except:
                return "failure"

    @staticmethod
    def updateSecurityQuestionAnswer(username, question, answer):
        
        try:
            User.replaceSecurityQuestion(username,question,question,answer)
            return "success"
        except:
            return "failure"

    @staticmethod
    def chooseSecurityQuestionForPrompt(username):
        questions = json.loads(crud.read("user","username",username,["securityQuestions"]))
        return choice(questions.keys())
    
    @staticmethod
    def checkIfSecurityQuestionResponseIsRight(username, question, answer):
        questions = json.loads(crud.read("user","username",username,["securityQuestions"]))
        return questions[question] == answer
    
    @staticmethod
    def replaceSecurityQuestion(username, old_question, new_question, answer):
        questions = json.loads(crud.read("user","username",username,["securityQuestions"]))
        questions.pop(old_question)
        questions[new_question] = answer
        questions = json.dumps(questions)
        crud.update('user','username',username,'securityQuestions',questions)
    
    @staticmethod
    def authentication(username: str, password: str):
        return password == crud.read("user","username",username,["password"])
    
    @staticmethod
    def isStudent(username):
        return "S" in crud.read("user","username",username,["accountType"])
    
    @staticmethod
    def isTeacher(username):
        return "T" in crud.read("user","username",username,["accountType"])
    
    @staticmethod
    def isAdmin(username):
        return "A" in crud.read("user","username",username,["accountType"])

class Course(Resource):
    
    def __init__(self):
        self.id = "" # created by sql itself. 
        self.coursename: string = ""
        self.coursedescription: string
        self.coursecapacity: int
        self.professor: string = ""
        self.students = []
        self.announcementInbox
    
    @staticmethod
    def create(coursename, coursedescription, coursecapacity, professor, students, announcementInbox):
        inputs = dict()
        inputs['coursename'] = coursename
        inputs['coursedescription'] = coursedescription
        inputs['coursecapacity'] = coursecapacity
        inputs['professor'] = professor
        inputs['students'] = students
        inputs['announcementInbox'] = ""
        crud.create("course", inputs)
        

class CreateAssignment(Resource):

    def put(self, name, description, points, duedate, courseid, student):
        Assignment.create_assignment(
                name,
                description,
                points,
                duedate,
                courseid,
                student)

class GetAssignment(Resource):

    def get(self,props=[],values=[]):
        return crud.search("announcements", props, values, )

class EditAssignment:
    def put(self, courseid,assignmentid, field, name):
        # GET ALL ASSIGNMENT IDS FOR COURSE
            students = crud.search('assignments',["courseid","assignmentid"],[courseid,assignmentid],["student"])
            return students
        # EDIT EACH
        # TODO 
class Assignment:

    @staticmethod
    def create_assignment(name, description, points, duedate, courseid, student):
        inputs = dict()
        #inputs['id'] = None 
        inputs['name'] = name
        inputs['description'] = description
        inputs['points'] = points
        inputs['duedate'] = duedate
        inputs['courseid'] = courseid
        # inputs['student'] = student
        crud.create('assignment', inputs)
    
    @staticmethod
    def edit_assignment(courseid, field, value):
        crud.update("assignment", "courseid", courseid, field, value)

    @staticmethod
    def grade_assignment():
        pass
    
    @staticmethod
    def submit_assignment():
        pass

class Announcements(Resource):

    def put(self, message, courseid):
        crud.create("announcements",{"message":message,"courseid":courseid,"senddate":date.today()})


api.add_resource(User, '/user/<string:accountType>/<string:password>/<string:username>/<string:securityQuestions>/<string:firstname>/<string:lastname>')



# Announcements Endpoints
api.add_resource(Announcements, "/announce/<string:courseid>/<string:message>")
