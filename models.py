from libs import * 
from constants import *
from forms import *

class CurrUser(UserMixin):
    id = ""

    def __init__(self, id) -> None:
        self.id = id