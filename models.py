from libs import * 
from constants import *
from forms import *

class User(UserMixin):
    email = ""
    password = ""
    name = ""
    id = ""

    def __init__(self, id, email, password, name) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name