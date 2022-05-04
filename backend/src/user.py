class User:
    
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.email = None
        self.accountType = None # subset of  "ATS" (s Student, t Teacher, a Admin)
        self.securityQuestions = dict()

    def createUser(self,userType=""):
        pass

    def getUserInfo(self):
        return vars(self)

    def updateSecurityQuestions(self):
        pass

    def login(self):
        # TODO Is this supposed to be in the frontend?
        pass

    def logout(self):
        # TODO Is this supposed to be in the frontend?
        pass

    def isStudent(self):
        pass

    def isTeacher(self):
        pass

    def isAdmin(self):
        pass
