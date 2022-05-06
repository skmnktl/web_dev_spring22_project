
class User:
    
    def __init__(self):
        self.id: int = None # number generated by sql
        self.password = None
        self.email = None
        self.accountType = None # subset of  "ATS" (s Student, t Teacher, a Admin)
        self.securityQuestions = dict()
        self.firstname
        self.lastname

        self.username = None # set equal to emai

        self.coursesAndAssignments = dict(list)


    def createUser(self,userType=""):
        pass

    def getUserInfo(self):
        return vars(self)

    def updateSecurityQuestionAnswer(self, question, answer):
        pass
    
    def chooseSecurityQuestionForPrompt(self):
        pass

    def replaceSecurityQuestion(self, old_question, new_question, answer):
        pass

    def authentication(self, username: string, password: string) -> Bool:
        pass

    def isStudent(self):
        return "S" in self.accountType 

    def isTeacher(self):
        return "T" in self.accountType 

    def isAdmin(self):
        return "A" in self.accountType 

    def write_to_db(self):
        pass
