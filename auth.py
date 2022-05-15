from libs import * 
from constants import *
from forms import *

auth = Blueprint('auth', __name__)


@auth.route(routeUrls["login"])
def login():
	return render_template("login.html")

@auth.route(routeUrls["login"], methods=['POST'])
def login_post():
    # login code goes here
    return redirect(url_for('main.hello'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

