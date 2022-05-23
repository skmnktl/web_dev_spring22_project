from libs import * 
from constants import *
from forms import *
from models import *

auth = Blueprint('auth', __name__)


@auth.route(routeUrls["login"])
def login():
    form = Login()
    email = None
    password = None
    return render_template("login.html",
                            form = form,
                            email = email,
                            password = password)

@auth.route(routeUrls["login"], methods=['POST'])
def login_post():
    # login code
    email    = request.form.get('email')
    password = request.form.get('password')

    # send username password
    params = [
                ("username",email),
                ("password", password)
            ]

    response = requests.post(apiUrls["login"], params=params)
    resp = json.loads(response.text)

    # check login and create user
    if bool(resp["login"]):
        user = CurrUser(int(resp["userid"]))
        login_user(user)
        return redirect(url_for('tempDash'))
    
    flash(resp["reason"])
    return redirect(url_for('auth.login'))


@auth.route(routeUrls['logout'])
@login_required
def logout(alias):
    if alias.user_id == current_user.id:
        # send username password
        params = [("userid", current_user.id)]
        #send logout request
        response = requests.post(apiUrls["logout"], params=params)
        resp = json.loads(response.text)
        if bool(resp.text):
            logout_user()
            flash('Logout Success!!')
        else:
            flash('User not logged in!!')
    return redirect(url_for('auth.login'))

