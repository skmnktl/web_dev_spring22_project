from libs import * 
from constants import *
from forms import *

class User(UserMixin):
    id = 0

    def __init__(self, id) -> None:
        self.id = id