import crud
import json
from random import choice
import typing
from datetime import date
from flask import Flask, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
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
    def post(self):
        print(request.args)
        props = request.args
        User.createUser(props['accountType'],
                        props['password'],
                        props['username'],
                        props['securityQuestions'],
                        props['firstname'],
                        props['lastname'])

api.add_resource(CreateUser, '/createuser')

class UpdateSecurityQuestionSchema(Schema):
    username = fields.Str(required = True)
    securityQuestions = fields.Str(required = True)

update_security_question = UpdateSecurityQuestionSchema() 

class UpdateSecurityQuestion(Resource):

    def post(self):
        props = request.args
        securityQuestions = props['securityQuestions']
        username = props['username']
        if securityQuestions=="":
            questions = dict()
        else:
            raw_questions = securityQuestions.split("<|>")
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
        userid   = request.args['userid']
        property = request.args['property']
        newValue = request.args['value']

        # if property=="securityQuestions":
        #     return "failure"
        # else:
        if property == "active":
            if newValue == "true":
                newValue = True
            else:
                newValue = False
        try:

            #update loggedIn table too with email
            if property == "username" or property == "email":
                crud.update("loggedIn",'email', userid, "email", newValue)

            
            User.changeUserData(userid, property, newValue)

            

            return {
                "response": True
            }

        except Exception as e:
            return {
                "response": False,
                "error": str(e)
            }


api.add_resource(UpdateUserData, "/updateuserdata")

class UpdateUserStatus(Resource):
    def post(self):
        print(f"[UPDATE] User Status")
        try:
            userid = request.args['userid']
            oldValue = json.loads(crud.search(
                                            'user',
                                            ["userid"],
                                            [userid],
                                            {"userid":"int"},
                                            ["active"]
                                            )
                                )[0][0]

            newValue = 1 if oldValue == 0 else 0
            User.changeUserData(userid,"active", newValue)
            # return f"The new value for user {userid} was {oldValue}, but it is now" +str(json.loads(crud.search('user',["userid"],[userid],{"userid":"int"},["active"]))) +"."

            return {
                "response": True,
                "newValue": newValue,
                "oldValue": oldValue
            }

        except Exception as e:
            return {
                "response": False,
                "error": str(e)
            }

api.add_resource(UpdateUserStatus, "/changeuserstatus")


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
        columns = ['userid','password','email','accountType','securityQuestions','firstname','lastname','active','username']
        #TODO: add fields required
        if len(row) > 0:
            return dict(zip(columns, row[0])), True
        else:
            return {}, False
    
    @staticmethod
    def changeUserData(userid, field, newValue):
        crud.update("user",'userid',userid, field, newValue)


    @staticmethod
    def parseQuestions(username):
        raw_questions = crud.read("user",
                                  "username",
                                  username,
                                  ["securityQuestions"])
        print(raw_questions)
        # in form of tuple
        # updated answers = a1<\>a2<\>a3
        raw_questions = raw_questions[0][0].split("<|>")
        # questions = dict([i.split("<?>") for i in raw_questions])
        return raw_questions
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
    def authentication(username: str, password: str) -> bool:
        #MODIFIED : Authenticate with hashed passsword
        print(password)
        print(check_password_hash(
                    crud.read("user","username",username,["password"])[0][0],
                    password))
        return check_password_hash(
                    crud.read("user","username",username,["password"])[0][0],
                    password)
    
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
    def create(coursename, coursedescription, coursecapacity, professor) -> bool:
        try:
            inputs = dict()
            inputs['coursename'] = coursename
            inputs['coursedescription'] = coursedescription
            inputs['coursecapacity'] = coursecapacity
            inputs['professor'] = professor
            inputs['students'] = ""
            inputs['announcementInbox'] = ""
            crud.create("course", inputs)
            return True
        except Exception as e:
            print("Error: {}".format(e))
            return False

class CreateCourse(Resource):
    def post(self):

        params = request.args

        if Course.create(params['coursename'],
                      params['coursedescription'],
                      params['coursecapacity'],
                      params['courseprofessor']):
            return True
        else:
            return False

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
        data = list(crud.read("course","courseid",courseid,None)[0])
        print(data)
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

class GetAllCourseIDs(Resource):
    def get(self):
        ids = json.loads(crud.search("course",["True"],["TRUE"],
                                                     dict([("True","int")]), ["courseid"]))
        return json.dumps({"courseids": [courseid for lst in ids for courseid in lst]})

api.add_resource(GetAllCourseIDs, "/getallcourseids")


class GetAllCourseIDsWithSpace(Resource):
    def get(self):
        ids = json.loads(crud.search("course",["True"],["TRUE"],dict([("True","int")]), ["courseid"]))
        ids = [str(i[0]) for i in ids]
        enrolled = []
        for id in ids:
            s = json.loads(crud.search("course", ["courseid"], [id], dict([("courseid","int")]), ["students"]))[0][0]
            s = len(s.split("<|>"))
            capacity = json.loads(crud.search("course", ["courseid"], [id], dict([("courseid","int")]), ["coursecapacity"]))[0][0]
            print(capacity)
            if s<capacity:
                enrolled.append((id,s))
        course_data = []
        for id,enrollment in enrolled:
            data = list(crud.read("course","courseid",id,None)[0])
            fields = ["courseid",'coursename',"coursedescription", "coursecapacity","professor","students"]
            dta = dict(list(zip(fields, data)))
            dta['enrolled'] = enrollment
            dta.pop("students",None)
            course_data.append(dta)
        return course_data


api.add_resource(GetAllCourseIDsWithSpace, "/getallcourseidswithcapacity")

class GetAllCourseIDsForStudent(Resource):
    def get(self):
        student = request.args["studentid"]
        search = \
        f"""
        SELECT courseid
        FROM course
        WHERE
            `students` LIKE \"%<|>{student}<|>%\"
            OR `students` LIKE \"{student}<|>%\"
            OR `students` LIKE \"%<|>{student}\"
            OR `students` = \"{student}\";
        """
        print(search)
        cursor = crud.conn.cursor()
        cursor.execute(search)
        result =  cursor.fetchall()
        return [courseid for lst in result for courseid in lst]

api.add_resource(GetAllCourseIDsForStudent,"/getallcourseidsforstudent")

class AddRemoveStudentCourse(Resource):

    def post(self):
            courseid = request.args['courseid']
            newValue = request.args['student']
            students = crud.read("course","courseid",courseid,["students"])
            students = students[0][0]
            if str(newValue) in students:
                s = students.split("<|>")
                s.remove(str(newValue))
                students = "<|>".join(s)
            newValue += "<|>" + students
            newValue = newValue.strip("<|>")
            crud.update('course','courseid',courseid,"students",newValue)

api.add_resource(AddRemoveStudentCourse, "/addremovestudentcourse")


class DeleteStudentFromCourse(Resource):

    def post(self):
        courseid = request.args['courseid']
        newValue = request.args['student']
        students = crud.read("course","courseid",courseid,["students"])
        students = students[0][0]
        students = students.replace(newValue,"").replace("<|><|>","<|>")
        students = students.strip("<|>")
        crud.update('course','courseid',courseid,"students",students)

api.add_resource(DeleteStudentFromCourse, "/deletestudentfromcourse")


class CreateAssignment(Resource):
    def post(self):
        try:
            inputs = ["assignmentid", "name", "description", "points", "duedate", "courseid"]
            values = dict([(i,request.args[i]) for i in inputs])
            courseid = request.args['courseid']
            students = crud.search("course",
                                    ["courseid"],
                                    [courseid],
                                    dict([("courseid","int")]),
                                    ["students"])
            students = json.loads(students)[0][0].split("<|>")
            print(students)
            for student in students:
                if student != "":
                    values["student"] = int(student)
                    crud.create("assignment", values)
                    
            return {
                    "response": True
                   }

        except Exception as e:
            return  {
                    "response": False,
                    "error"   : str(e)
                    }

api.add_resource(CreateAssignment,"/createassignment")


class GetAssignments(Resource):
    def get(self):
        try:
            courseid =  request.args["courseid"]
            types = dict([("name","str"),
                        ("description","str"),
                        ("points","int"),
                        ("duedate","str"),
                        ("courseid","int"),
                        ("student","str"),
                        ("assignmentid","int")])
            data = crud.search("assignment", ["courseid"], [courseid], types, None)
            data = json.loads(data)
            print(data)
            result = {}
            for line in data:
                if line[0] not in result.keys():
                    # not needed                    
                    result[line[0]] = line[:-2]
            return {
                    "response": True,
                    "data"    : result
            }
        except Exception as e:
            return  {
                    "response": False,
                    "error"   : str(e)
                }

api.add_resource(GetAssignments, "/getassignments")

class GetAllAssignmentsStudent(Resource):
    def get(self):
        try:
            studentid =  request.args["userid"]
            types = dict([("name","str"),
                        ("description","str"),
                        ("points","int"),
                        ("duedate","str"),
                        ("courseid","int"),
                        ("student","str"),
                        ("assignmentid","int")])
            data = crud.search("assignment", ["student"], [studentid], types, None)
            data = json.loads(data)
            print(data)
            result = {}
            for line in data:
                if line[0] not in result.keys():
                    # not needed                    
                    result[line[0]] = line[:-2]
            return {
                    "response": True,
                    "data"    : result
            }
        except Exception as e:
            return  {
                    "response": False,
                    "error"   : str(e)
                }

api.add_resource(GetAllAssignmentsStudent, "/getallassignmentsstudent")


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

class CountCourses(Resource):
    def get(self):
        ids = json.loads(crud.search("course",["True"],["TRUE"],
                                                             dict([("True","int")]), ["courseid"]))
        return len(list(set([courseid for lst in ids for courseid in lst])))

api.add_resource(CountCourses,"/countcourses")

class ActiveStudents(Resource):
    def get(self):
        students = json.loads(crud.search('user',
                                   ["accountType"],
                                   ["S"],
                                   {"accountType":"str"},
                                   ["userid",'active']))
        students2 = json.loads(crud.search('user',
                                           ["accountType"],
                                           ["student"],
                                           {"accountType":"str"},
                                           ["userid",'active']))
        s = dict(students+students2)
        filtered = [1 for i in s.items() if i[1]]
        return sum(filtered)

api.add_resource(ActiveStudents, "/countactivestudents")


def concat(l1, l2):
    return l1.extend(l2)

class ActiveTeachers(Resource):
    def get(self):
        teachers = json.loads(crud.search('user',
                                   ["accountType"],
                                   ["T"],
                                   {"accountType":"str"},
                                   ["userid",'active']))
        teachers2 = json.loads(crud.search('user',
                                           ["accountType"],
                                           ["TA"],
                                           {"accountType":"str"},
                                           ["userid",'active']))
        teachers3 = json.loads(crud.search('user',
                                                   ["accountType"],
                                                   ["TA"],
                                                   {"accountType":"str"},
                                                   ["userid",'active']))
        t = dict(teachers + teachers2 + teachers3)
        filtered = [1 for i in t.items() if i[1]]
        return sum(filtered)

api.add_resource(ActiveTeachers, "/countactiveteachers")


class AllUsers(Resource):
    def get(self):
        users = json.loads(crud.search(
            'user',
            ["TRUE"],
            ["TRUE"],
            {"TRUE":"int"},
            None)
        )
        allfields = ['userid','pass',"email","accountType","securityQuestions","firstname","lastname","active","username"]
        userDicts = []
        fields = ['userid',"email","accountType","firstname","lastname","active"]
        for user in users:
            userDicts.append(dict([i for i in list(zip(allfields,user)) if i[0] in fields]))
        return userDicts

api.add_resource(AllUsers, "/allusers")

class GetUser(Resource):
    def get(self):
        userid = request.args['userid']
        user = json.loads(crud.search('user',
                                   ["userid"],
                                   [userid],
                                   {"userid":"int"},
                                   None))[0]
        allfields = ['userid','pass',"email","accountType","securityQuestions","firstname","lastname","active","username"]
        fields = ['userid',"email","accountType","firstname","lastname","active"]
        return dict([i for i in list(zip(allfields,user)) if i[0] in fields])

api.add_resource(GetUser, "/getuser")


class GetQuestions(Resource):
    def get(self):
        return User.parseQuestions(request.args['email'])

api.add_resource(GetQuestions, "/getquestions")



def getStudentsInCourseForAssignment(courseid):
    students = crud.search('assignments',
                           ["courseid"],
                           [courseid],
                           ["int"],
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
            courseid = request.args['courseid']
            students = json.loads(crud.search("course",
                                      ["courseid"],
                                      [courseid],
                                      dict([("courseid","int")]),
                                      ["students"]))
            for s in students:
                crud.update("assignment", "courseid", courseid, field, value)
            return students

api.add_resource(GradeAssignment,"/gradeassignment")

class PostAnnouncement(Resource):
    def post(self):
        courseid = request.args['courseid']
        message = request.args['message']
        crud.create("announcements",{"message":message,"courseid":courseid,"senddate":str(date.today())})

api.add_resource(PostAnnouncement, "/postannouncement")

class GetAnnouncements(Resource):
    def get(self):
        courseid = request.args['courseid']
        announcements = json.loads(crud.search("announcements",
                                               ["courseid"],
                                               [courseid],
                                               dict([("courseid","int")]),
                                               None))
        announcementsList = []
        for announcement in announcements:
            announcementsList.append({
                                        "message":announcement[1],
                                        "announcementid":announcement[0],
                                        "date":announcement[2]
                                    })
        return announcementsList

api.add_resource(GetAnnouncements, "/getannouncements")

# login classes
# EDITED - hardikajmani

# login user -> adds the user to login table
class LoginUser(Resource):
    def post(self):
        """
            gets username and password
            sends back the id to logg in
        """
        props = request.args

        #1. check if user exists
        user, resp = User.getUserInfo(props["username"])

        # if user doesnt exist or incorrect password
        if not (resp):
            return json.dumps({
                                "login": False,
                                "reason": "User Not Found"
                    })
        

        # check if user is acitve 
        if user["active"] != 1:
            return json.dumps({
                        "login": False,
                        "reason": "User Not Activated. Contact Admin!"
                    })
        

        if not User.authentication(props["username"], props["password"]):
            return json.dumps({
                        "login": False,
                        "reason": "Incorrect Pass"
                    })
        
        try:
            crud.create("loggedIn", {
                "userid": int(user["userid"]),
                "password": user["password"],
                "email": user["email"]
            })

            return json.dumps({
                                "login"  : True,
                                "userid" : int(user["userid"]),
                                "accountType": user["accountType"]
                            })
        except Exception as e:
            return json.dumps({
                                "login": False,
                                "reason": str(e)
                            })

        

api.add_resource(LoginUser, "/login")

# verifies user is logged in -> checks the id in login_table
class VerifyLoginUser(Resource):
    def post(self):
        """
            Gets a response in return for id, whether
            user exists in loggedin table or not
        """
        row = crud.read("loggedIn","userid", request.args["userid"])
        if len(row) > 0:
             #1. check if user exists
            user, resp = User.getUserInfo(row[0][2]) #username
            if resp:
                return json.dumps(
                    {
                        "status": True,
                        "accountType": user["accountType"] 
                    }
                )
            else:
                return json.dumps(
                {
                    "status": False
                }
            )
        else:
            return json.dumps(
                {
                    "status": False
                }
            )

api.add_resource(VerifyLoginUser, "/verifylogin")


# verify user
class VerifyUser(Resource):
    def get(self):
        """
            Gets a response if user exist or not
        """
        #1. check if user exists
        user, resp = User.getUserInfo(request.args["email"]) #username

        return {
            "response": resp,
            "userid":  user["userid"] if resp else -1
        }


api.add_resource(VerifyUser, "/verifyuser")


class VerifyPassword(Resource):
    def get(self):
        """
            Gets a response if user exist or not
        """
        row = crud.read("user","userid", request.args["userid"])
        if len(row) > 0:
            #1. validate pass
            resp = User.authentication(row[0][2], request.args["password"]) #username
            return {
                "response": resp
            }

        return {
                "response": False,
                "error": "User doesnot exist"
            }
        
api.add_resource(VerifyPassword, "/verifypass")


# logout user -> removes the user from login table
class LogoutUser(Resource):
    def post(self):
        # check if user is logged in
        row = crud.read("loggedIn","userid", request.args["userid"])
        if len(row) > 0:
            crud.delete("loggedIn","userid", request.args["userid"])
            return True
        else:
            return False

api.add_resource(LogoutUser, "/logout")



class HelloWorld(Resource):
    def get(self):
        return "Hello World!"

# Hello World
api.add_resource(HelloWorld, "/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3310)
