from libs import * 
from constants import *
from forms import *

main = Blueprint('main', __name__)

# http://127.0.0.1:5000/
@main.route(routeUrls["main"])
def home():
    return "Hello, Flask!"

# sample :removeit
@main.route("/hello")
@login_required
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=current_user.name,
        date=datetime.now()
    )
