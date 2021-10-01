####################################
# File name: __init__.py           #
# Author: Joe Abbate               #
####################################
from subprocess import check_output
import datetime
import os
from flask_mail import Mail, Message
import pytz
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask import Flask, render_template, send_from_directory, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, logout_user, login_required, LoginManager, current_user

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

# Commit
commit = check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').rstrip()

# pylint: disable=wrong-import-position
from lights.models import User, Seat
#from rides.forms import EventForm, CarForm
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
@app.route('/')
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
    if auth_dict is None:
        return redirect(url_for('login'))
    q = User.query.get(auth_dict['uid'])
    if q is not None:
        g.user = q # pylint: disable=assigning-non-slot
    else:
        user = User(auth_dict['uid'], "SOLID", "7700ff",
            None, None, None, None)
        g.user = user # pylint: disable=assigning-non-slot
        db.session.add(user)

    db.session.commit()
    login_user(g.user)
    return redirect(url_for('index'))


# Application
@app.route('/home')
@login_required
def index():
    return render_template('index.html')
