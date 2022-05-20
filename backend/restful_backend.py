import crud
import json
from random import choice
from datetime import date
from flask import Flask, request, abort
from flask_restful import Resource, Api
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


class AuthenticateUser(Resource):
    def get(self):
        username = request.args['username']
        password = request.args['password']
        return User.authentication(username,password)

api.add_resource(AuthenticateUser,"/userauth")

class AccountType(Resource):
    def get(self):
        username = request.args['username']
        permissions = request.args['permissions']
        if permissions=="student":
            return User.isStudent(username)
        if permissions=="teacher":
            return User.isTeacher(username)
        if permissions=="admin":
            return User.isAdmin(username)
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
        raw_questions = crud.read("user","username",username,["securityQuestions"])
        print(raw_questions)
        return "PAUSE"
        raw_questions = raw_questions.split("<|>")
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

class Course:
    @staticmethod
    def create(coursename, coursedescription, coursecapacity, professor, students):
        inputs = dict()
        inputs['coursename'] = coursename
        inputs['coursedescription'] = coursedescription
        inputs['coursecapacity'] = coursecapacity
        inputs['professor'] = professor
        inputs['students'] = students
        inputs['announcementInbox'] = ""
        crud.create("course", inputs)

class CreateCourse(Resource):
    def post(self):
        params = request.args
        Course.create(params['coursename'],
                      params['coursedescription'],
                      params['coursecapacity'],
                      params['professor'],
                      params['students'])

api.add_resource(CreateCourse, "/createcourse")

class EditCourse(Resource):
    def put(self):
        courseid = request.args['courseid']
        field = request.args['field']
        newValue = request.args['newValue']
        crud.update('course','courseid',courseid,field,newValue)

api.add_resource(EditCourse,"/editcourse")

class GetCourse(Resource):
    def get(self):
        courseid = request.args['courseid']
        data = list(crud.read("course","courseid",courseid,None))
        fields = ["courseid",'coursename',"coursedescription",
                  "coursecapacity","professor","students"]
        return json.dumps(dict(list(zip(fields, data))))


api.add_resource(GetCourse,"/getcourse")

class GetStudentsInCourse(Resource):
    def get(self):
        courseid = request.args['courseid']
        return json.loads(crud.search("course",
                                      ["courseid"],
                                      [courseid],
                                      dict([("courseid","int")]),
                                      ["students"]))

api.add_resource(GetStudentsInCourse, "/getstudentsenrolledincourse")

class AddStudentToCourse(Resource):

    def put(self):
        courseid = request.args['courseid']
        newValue = request.args['student']
        students = crud.read("course","courseid",courseid,["students"])
        students = students[0][0]
        newValue += "<|>" + students
        newValue = newValue.strip("<|>")
        crud.update('course','courseid',courseid,"students",newValue)

api.add_resource(AddStudentToCourse, "/addstudenttocourse")

class DeleteStudentFromCourse(Resource):

    def put(self):
        courseid = request.args['courseid']
        newValue = request.args['student']
        students = crud.read("course","courseid",courseid,["students"])
        students = students[0][0]
        students = students.replace(newValue,"").replace("<|><|>","<|>")
        students = students.strip("<|>")
        crud.update('course','courseid',courseid,"students",students)

api.add_resource(DeleteStudentFromCourse, "/deletestudentfromcourse")

class CreateAssignment(Resource):

    def put(self):
        inputs = ["name","description","points","duedate","courseid",
                  "student","assignmentid"]
        values = dict([(i,request.args[i]) for i in inputs])
        crud.create("assignment", values)

api.add_resource(CreateAssignment,"/createassignment")

class GetAssignments(Resource):

    def get(self):
        data = request.args["props"].split("<|>")
        data = dict([d.split("<?>") for d in data])
        props = data.keys()
        values = data.values()
        types = dict([("name","str"),
                      ("description","str"),
                      ("points","int"),
                      ("duedate","str"),
                      ("courseid","int"),
                      ("student","str"),
                      ("assignmentid","int")])

        if len(props) != len(values): return "Incorrect number of property names and values"
        data = crud.search("assignment", props, values,types, None)
        data = json.loads(data)
        fields = sorted(types.keys())
        result = []
        for line in data:
            d = dict(zip(fields,line))
            result.append(d)
        return result

api.add_resource(GetAssignments, "/getassignments")

class EditAssignment(Resource):
    def put(self, courseid,assignmentid, field, value):
        if field=="points":
            value = int(value)
        # GET ALL ASSIGNMENT IDS FOR COURSE
            students = getStudentsInCourseForAssignment(courseid)
            print(students)
            for s in students:
                crud.update("assignment", "courseid", courseid, field, value)
            return students

api.add_resource(EditAssignment,"/editassign")


def getStudentsInCourseForAssignment(courseid):
    students = crud.search('assignments',
                           ["courseid"],
                           [courseid],
                           ["int"]
                           ["student"])
    return list(set(json.loads(students)))


def getStudentsInCourseAssignments(courseid, assignmentid):
    students = crud.search('assignments',
                           ["courseid","assignmentid"],
                           [courseid,assignmentid],
                           ["int","int"],
                           ["student"])
    return set(list(json.loads(students)))

class GradeAssignment(Resource):
    def put(self, courseid,assignmentid, field, value):
        if field=="points":
            value = int(value)
            students = getStudentsInCourse(courseid)
            for s in students:
                crud.update("assignment", "courseid", courseid, field, value)
            return students

api.add_resource(GradeAssignment,"/gradeassignment")

class PostAnnouncement(Resource):

    def post(self, courseid: int, message):
        courseid = request.args['courseid']
        crud.create("announcements",{"message":message,"course":courseid,"senddate":str(date.today())})


api.add_resource(PostAnnouncement, "/announce")


class HelloWorld(Resource):
    def get(self):
        return "Hello World!"

# Hello World
api.add_resource(HelloWorld, "/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3310)
