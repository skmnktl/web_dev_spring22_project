from libs import * 
from constants import *
from forms import *

class User(UserMixin):
    id = 0
    accountType = ""

    def __init__(self, id, accountType) -> None:
        self.id = id
        self.accountType = accountType

    def is_admin(self) -> bool:
        return self.accountType == "admin"

    def returnAccountType(self):
        return self.accountType