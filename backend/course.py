import crud

class Course:
    
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
        

class Assignment:
    
    def __init__(self):
        self.id
        self.name 
        self.description
        self.points
        self.duedate
        self.courseid
        self.student

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

    def grade_assignment():
        pass

    def submit_assignment():
        pass


def create_assignment(name, descriptions, duedate, course, numberofpoints, students: list):
    pass

class Announcements:
    self.message
    self.date
    self.course 

    @staticmethod
    def new_message():
        pass
