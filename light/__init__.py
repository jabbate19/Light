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
import time

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
from light.models import User, Seat, Room
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
@app.route('/login')
@app.route('/')
@auth.oidc_auth('default')
@csh_user_auth
def csh_auth(auth_dict=None):
    if auth_dict is None:
        return redirect(app.config["SERVER_NAME"]+"/csh-auth")
    q = User.query.get(auth_dict['uid'])
    if q is not None:
        q.firstname = auth_dict['first']
        q.lastname = auth_dict['last']
        q.picture = auth_dict['picture']
        g.user = q # pylint: disable=assigning-non-slot
    else:
        user = User(auth_dict['uid'], auth_dict['first'], auth_dict['last'], auth_dict['picture'], "SOLID", "#B0197E",
            None, None, None, None)
        g.user = user # pylint: disable=assigning-non-slot
        db.session.add(user)
    db.session.commit()
    login_user(g.user)
    return redirect(url_for('index'))


# Application
@app.route('/seats')
@login_required
def seats():
    seats = Seat.query.all()
    seat_users = []
    for seat in seats:
        seat_users.append( seat.user )
    return render_template('seats.html', users = seat_users, num_seats = len(seat_users) )

# Application
@app.route('/home')
@login_required
def index():
    rooms = Room.query.all()
    return render_template('index.html', rooms = rooms )


def update_pi( ip ):
    # Pi notifying socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, 4444))
        msg = "UPDATE"
        s.send(msg.encode())
        s.close()
    except Exception as e:
        print("Pi Send Error:", e)
        s.close()


@app.route("/claim/<position>", methods=['GET', 'POST'])
@login_required
def claim(position):
    seat = Seat.query.get( int(position) )
    seat.user = current_user.id
    seat.style = current_user.style
    seat.numcolors = current_user.numcolors      
    seat.color1 = current_user.color1
    seat.color2 = current_user.color2
    seat.color3 = current_user.color3
    db.session.commit()
    update_pi( position )
    return redirect(url_for('index'))


@app.route("/leave/<position>", methods=['GET', 'POST'])
@login_required
def leave(position):
    seat = Seat.query.get( int(position) )
    seat.user = None
    seat.style = None
    seat.numcolors = None   
    seat.color1 = None
    seat.color2 = None
    seat.color3 = None
    db.session.commit()
    update_pi( position )
    return redirect(url_for('index'))

@app.route("/room/<room_id>", methods=['GET', 'POST'])
@login_required
def edit_room( room_id ):
    form = ColorForm()
    room = Room.query.get( room_id )
    if form.validate_on_submit():
        room.style = form.style.data
        room.numcolors = form.numcolors.data
        room.color1 = form.color1.data
        room.color2 = form.color2.data
        room.color3 = form.color3.data
        room.last_modify_user = current_user.id
        room.last_modify_time = time.strftime("%H:%M:%S", time.localtime() )
        db.session.commit()
        update_pi( room.pi_ip )
        return redirect(url_for('index'))
    return render_template('colorform.html', form=form, current_style=room.style, current_num=room.numcolors, current_c1=room.color1, current_c2=room.color2, current_c3=room.color3)

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
        seat = Seat.query.filter(Seat.user == current_user.id).first()
        if seat:
            seat.style = form.style.data
            seat.numcolors = form.numcolors.data
            seat.color1 = form.color1.data
            seat.color2 = form.color2.data
            seat.color3 = form.color3.data
        db.session.commit()
        if seat:
            update_pi( str(seat.id) )
        return redirect(url_for('index'))
    return render_template('colorform.html', form=form, current_style=current_user.style, current_num=current_user.numcolors, current_c1=current_user.color1, current_c2=current_user.color2, current_c3=current_user.color3)