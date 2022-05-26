from libs import * 
from constants import *
from forms import *
from models import *

auth = Blueprint('auth', __name__)


@auth.route(routeUrls["login"], methods=['GET','POST'])
def login():
    form = Login()
    email = form.email.data
    password = form.password.data

    if current_user.is_authenticated:
        return redirect(url_for('tempDash'))

    if form.validate_on_submit():
        # send username password
        params = [
            ("username",email),
            ("password", password)
        ]

        response = requests.post(apiUrls["login"], params=params)
        resp = json.loads(response.text)
        resp = json.loads(resp)
        # check login and create user
        if resp["login"]:
            user = User(int(resp["userid"]), resp["accountType"])
            login_user(user)
            print(current_user.get_id())
            print(current_user.is_authenticated)
            print(current_user.is_admin())
            print(current_user.returnAccountType())
            return redirect(url_for('tempDash'))
        
        flash(resp["reason"])
        return redirect(url_for('auth.login'))


    return render_template("login.html",
                            form = form,
                            email = email,
                            password = password)

# @auth.route(routeUrls["login"], )
# def login_post():
#     # login code
#     email    = request.form.get('email')
#     password = request.form.get('password')


    
    
    

@auth.route(routeUrls['logout'])
@login_required
def logout():
    # send current user id
    params = [("userid", current_user.id)]
    #send logout request
    response = requests.post(apiUrls["logout"], params=params)
    if json.loads(response.text):
        logout_user()
        flash('Logout Success!!')
    else:
        flash('User not logged in!!')
    return redirect(url_for('auth.login'))

