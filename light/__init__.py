####################################
# File name: __init__.py           #
# Author: Joe Abbate               #
####################################
from subprocess import check_output
import datetime
import os
import socket
import pytz
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask import Flask, render_template, send_from_directory, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from config import PI_IP

# Setting up Flask and csrf token for forms.
app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

# Establish SQL Database
db = SQLAlchemy(app)

# OIDC Authentication
CSH_AUTH = ProviderConfiguration(issuer=app.config["OIDC_ISSUER"],
                                 client_metadata=ClientMetadata(
                                     app.config["OIDC_CLIENT_ID"],
                                     app.config["OIDC_CLIENT_SECRET"]))
auth = OIDCAuthentication({'default': CSH_AUTH},
                          app)

auth.init_app(app)

# Flask-Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Pi notifying socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Commit
commit = check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').rstrip()

# pylint: disable=wrong-import-position
from light.models import User, Seat
from light.forms import ColorForm
from .utils import csh_user_auth

# time setup for the server side time
eastern = pytz.timezone('US/Eastern')
fmt = '%Y-%m-%d %H:%M'

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/assets'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Demo page, not neded for use
@app.route('/demo')
def demo(auth_dict=None):
    # Get current EST time.
    loc_dt = datetime.datetime.now(tz=eastern)
    st = loc_dt.strftime(fmt)
    return render_template('demo.html', timestamp=st, datetime=datetime, auth_dict=auth_dict)


# LOG IN MANAGEMENT
@app.route('/login')
def login(auth_dict=None):
    return redirect(url_for('csh_auth'))


@login_manager.user_loader
def load_user(user_id):
    q = User.query.get(user_id)
    if q:
        return q
    return None


@app.route("/logout")
@auth.oidc_logout
def _logout():
    logout_user()
    return redirect("/", 302)


@app.route('/csh-auth')
@app.route('/')
@auth.oidc_auth('default')
@csh_user_auth
def csh_auth(auth_dict=None):
    print("b")
    if auth_dict is None:
        return redirect(app.config["SERVER_NAME"]+"/csh-auth")
    q = User.query.get(auth_dict['uid'])
    if q is not None:
        print("c")
        q.firstname = auth_dict['first']
        q.lastname = auth_dict['last']
        q.picture = auth_dict['picture']
        g.user = q # pylint: disable=assigning-non-slot
    else:
        print("d")
        user = User(auth_dict['uid'], auth_dict['first'], auth_dict['last'], auth_dict['picture'], "SOLID", "#B0197E",
            None, None, None, None)
        g.user = user # pylint: disable=assigning-non-slot
        db.session.add(user)
    print("e")
    db.session.commit()
    login_user(g.user)
    return redirect(url_for('index'))


# Application
@app.route('/home')
@login_required
def index():
    return render_template('index.html')

def update_pi():
    s.connect((app.config['PI_IP'], app.config['PI_PORT']))
    s.send("UPDATE".encode())
    s.close()

@app.route("/colorform", methods=['GET', 'POST'])
@login_required
def edit_colors():
    form = ColorForm()
    if form.validate_on_submit():
        current_user.style = form.style.data
        current_user.numcolors = form.numcolors.data
        current_user.color1 = form.color1.data
        current_user.color2 = form.color2.data
        current_user.color3 = form.color3.data
        seats = Seat.query.filter(Seat.user == current_user.id).all()
        if seats:
            seat = seats[0]
            seat.style = form.style.data
            seat.numcolors = form.numcolors.data
            seat.color1 = form.color1.data
            seat.color2 = form.color2.data
            seat.color3 = form.color3.data
            db.session.add(seat)
        db.session.add(current_user)
        db.session.commit()
        if seats:
            update_pi()
        return redirect(url_for('index'))
    return render_template('colorform.html', form=form, current_style=current_user.style, current_num=current_user.numcolors, current_c1=current_user.color1, current_c2=current_user.color2, current_c3=current_user.color3)