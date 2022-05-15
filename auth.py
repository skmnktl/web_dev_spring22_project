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
    # login code goes here
    email    = request.form.get('email')
    password = request.form.get('password')

    print("password : {}".format(password))
    print("hasehd password : {}".format(generate_password_hash(password, method='sha256')))
    print("hasehd test : {}".format(generate_password_hash(test_pass, method='sha256')))
    if check_password_hash(generate_password_hash(test_pass, method='sha256'), password):
        time.sleep(2)
        user = User(1, test_email, generate_password_hash(test_pass, method='sha256'), "hardik")
        login_user(user)
        return redirect(url_for('main.hello'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login'))

@auth.route(routeUrls['logout'])
@login_required
def logout():
    logout_user()
    flash('Logout Success!!')
    return redirect(url_for('auth.login'))

