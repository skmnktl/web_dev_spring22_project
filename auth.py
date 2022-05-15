from libs import * 
from constants import *
from forms import *

auth = Blueprint('auth', __name__)

# http://127.0.0.1:5000/login
@auth.route(routeUrls["login"])
def login():
	return render_template("login.html")

@auth.route(routeUrls["login"], methods=['POST'])
def login_post():
    # login code goes here
    return redirect(url_for('main.profile'))

