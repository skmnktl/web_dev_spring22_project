from libs import * 
from constants import *
from forms import *

class User(UserMixin):
    email = ""
    password = ""
    name = ""

    def __init__(self, email, password, name) -> None:
        self.email = email
        self.password = password
        self.name = name