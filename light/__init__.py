####################################
# File name: __init__.py           #
# Author: Joe Abbate               #
####################################
from subprocess import check_output
from datetime import datetime
import os
import socket
import pytz
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask import Flask, render_template, send_from_directory, redirect, url_for, g, request
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
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
migrate = Migrate(app, db)
socketio = SocketIO(app)

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
from .models import User, Room
from .forms import ColorForm, RoomForm
from .utils import csh_user_auth

# time setup for the server side time
eastern = pytz.timezone('America/New_York')
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
        user = User(auth_dict['uid'], auth_dict['first'], auth_dict['last'], auth_dict['picture'])
        g.user = user # pylint: disable=assigning-non-slot
        db.session.add(user)
    db.session.commit()
    login_user(g.user)
    return redirect(url_for('index'))

# Application
@app.route('/home')
@login_required
def index():
    return render_template('index.html', rooms = active_user_query().all() )

@socketio.on('connect')
def pi_connect():
    sid = request.sid
    print("Connect on",sid)
    
@socketio.on('disconnect')
def pi_disconnect():
    sid = request.sid
    print("Disconnect on",sid)
    room = Room.query.filter(Room.session_id == sid).first()
    if room:
        room.session_id = None
    db.session.commit()

@socketio.on('login')
def pi_name(data):
    print(data)
    sid = request.sid
    attempted_room = Room.query.get(data['name'])
    if attempted_room:
        if attempted_room.mac == data['pass']:
            if attempted_room.session_id:
                emit('login error', {'data':'Device Already Connected Under This Login'})
            else:
                attempted_room.session_id = sid
                db.session.commit()
                emit('light',  {'style':attempted_room.style,'color1':attempted_room.color1,'color2':attempted_room.color2,'color3':attempted_room.color3})
        else:
            emit('login error', {'data':'Invalid Password'})
    else:
        emit('login error', {'data':'Invalid User'})
    
def active_user_query(name = None):
    return Room.query.filter(Room.session_id.isnot(None))

def data_change(cmd, sid):
    socketio.emit( 'light', cmd, to=sid)

@app.route("/room/<room_id>", methods=['GET', 'POST'])
@login_required
def edit_room( room_id ):
    room = Room.query.get(room_id)
    if not room:
        return 404
    if not room.session_id:
        return 404
    form = ColorForm()
    if form.validate_on_submit():
        numcolors = form.numcolors.data
        style = form.style.data
        if style == "BLINK" or style == "CHASE" or style == "COMET" or style == "PULSE":
            style += numcolors
        room.style = style
        room.color1 = form.color1.data
        room.color2 = form.color2.data
        room.color3 = form.color3.data
        room.last_modify_user = current_user.id
        room.last_modify_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        db.session.commit()
        cmd = { 'style':style,'color1':form.color1.data,'color2':form.color2.data,'color3':form.color3.data }
        data_change(cmd, room.session_id)
        return redirect(url_for('index'))
    return render_template('colorform.html', form=form, current_style=room.style, current_c1=room.color1, current_c2=room.color2, current_c3=room.color3)

@app.route("/add_room", methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room( form.name.data, form.mac_addr.data )
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('roomform.html', form=form, name = '', mac_addr = '')

@app.route("/delete_room/<room_id>", methods=['GET'])
def del_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return 404
    db.session.delete(room)
    db.session.commit()
    return redirect('/')