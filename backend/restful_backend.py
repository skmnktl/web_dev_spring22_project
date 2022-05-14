import crud
import json
from random import choice
from datetime import date
from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_restful import reqparse
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)

USER_FIELDS = ['password','email','accountType','securityQuestions','firstname','lastname','username','active']

class CreateUserSchema(Schema):
        accountType = fields.Str(required=True)
        password = fields.Str(required=True)
        username = fields.Str(required=True)
        securityQuestions = fields.Str(required=True)
        firstname = fields.Str(required=True)
        lastname = fields.Str(required=True)

create_user_schema =  CreateUserSchema()

class CreateUser(Resource):

    def get(self):
        props = request.args
        User.createUser(props['accountType'], props['password'], props['username'], props['securityQuestions'], props['firstname'], props['lastname'])
        securityObj = UpdateSecurityQuestion()
        securityObj.post(props) # inefficient more data is passed than necessary...
        return "success"

api.add_resource(CreateUser, '/createuser')

class UpdateSecurityQuestionSchema(Schema):
    username = fields.Str(required = True)
    securityQuestions = fields.Str(required = True)

update_security_question = UpdateSecurityQuestionSchema() 

class UpdateSecurityQuestion(Resource):

    def post(self, props=None):
        if props is None:
            props = request.args
        securityQuestions = props['securityQuestions']
        username = props['username']
        raw_questions = securityQuestions.split("<|>")
        if raw_questions=="":
            questions = dict()
        else:
            questions = dict([i.split("<?>") for i in raw_questions])
        
        for q in  questions.keys():
            a = questions[q]
            User.replaceSecurityQuestion(username, q, q, a)
        
api.add_resource(UpdateSecurityQuestion,"/updatesecurityquestion")

class UpdateUserDataSchema:
    username = fields.Str(required = True)
    property = fields.Str(required = True)
    value = fields.Str(required = True)

class UpdateUserData(Resource):
    def post(self):
        username = request.args['username']
        property = request.args['property']
        newValue = request.args['value']

        if property=="securityQuestions":
            return "failure"
        else:
            if property == "active":
                if newValue == "true":
                    newValue = True
                else:
                    newValue = False
            User.changeUserData(username,property, newValue)

api.add_resource(UpdateUserData, "/updateuserdata")

class User:

    @staticmethod
    def createUser(accountType, password, username, securityQuestions, firstname, lastname):
        
        #securityQuestions = json.dumps(securityQuestions)
        values = [password, username, accountType, securityQuestions, firstname, lastname, username, True]
        
        inputs = dict()
        for k,v in zip(USER_FIELDS,values):
            inputs[k] = v
        try:
            crud.create("user", inputs)
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
    def parseQuestions(username):
        raw_questions = crud.read("user","username",username,["securityQuestions"]).split("<|>")
        questions = dict([i.split("<?>") for i in raw_questions])
        return questions
    # question1<*>answer1<|>question2<*>answer2
    @staticmethod
    def chooseSecurityQuestionForPrompt(username):
        questions = User.parseQuestions(username)
        return choice(questions.keys())
    
    @staticmethod
    def checkIfSecurityQuestionResponseIsRight(username, question, answer):
        questions = User.parseQuestions(username)
        return questions[question] == answer
    
    @staticmethod
    def replaceSecurityQuestion(username, old_question, new_question, answer):
        questions = User.parseQuestions(username)
        if questions.get(old_question,None):
            questions.pop(old_question)
        questions[new_question] = answer
        new_questions = ""
        for key in questions.keys():
            new_questions+= f"{key}<*>{questions[key]}<|>"
        crud.update('user','username',username,'securityQuestions',new_questions)
    
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

class Course():
    
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
       

def edit_assignment(courseid, field, value):
        crud.update("assignment", "courseid", courseid, field, value)

class CreateAssignment(Resource):

    def put(self, name, description, points, duedate, courseid, student):
        inputs = ["name","description","points","duedate","courseid","student"]
        values = [name, description, int(points), duedate, courseid, student]
        crud.create("assignments", inputs, values)

api.add_resource(CreateAssignment,"/createassignment/<string:name>/<string:description>/<int:points>/<string:duedate>/<int:courseid>/<int:student>")

class GetAssignment(Resource):

    def get(self,props,values):
        props = props.split("<|>")
        values = values.split("<|>")
        if len(props) != len(values): return "Incorrect number of property names and values"
        for ind,val in enumerate(props):
            if val=="points":
                values[ind]=int(values[ind])
        return crud.search("announcements", props, values,None)

api.add_resource(GetAssignment, "/getassignment/<string:props>/<string:values>")


class EditAssignment(Resource):
    def put(self, courseid,assignmentid, field, value):
        if field=="points":
            value = int(value)
        # GET ALL ASSIGNMENT IDS FOR COURSE
            students = crud.search('assignments',["courseid","assignmentid"],[courseid,assignmentid],["student"])
            return students

api.add_resource(EditAssignment,"/editassign/<int:courseid>/<int:id>/<string:field>/<string:value>")

class GradeAssignment(Resource):
    pass

class PostAnnouncement(Resource):

    def post(self, courseid: int, message):
        try:
            crud.create("announcements",{"message":message,"course":courseid,"senddate":str(date.today())})
            return "success"
        except:
            return "failure"


api.add_resource(PostAnnouncement, "/announce/<int:courseid>/<string:message>")


class HelloWorld(Resource):
    def get(self):
        return "Hello World!"

# Hello World
api.add_resource(HelloWorld, "/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3310)
